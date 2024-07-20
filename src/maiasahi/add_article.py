import asyncio
from datetime import datetime
import json
import logging
from pathlib import Path
import random
import re

from typing import Any, cast

import aiofiles
import requests
from bs4 import BeautifulSoup, Tag
from jinja2 import Environment, PackageLoader

from .asahi import sections, get_links
from .add_audio import add_audio_from_article
from .chatgpt import annotate_article

logger = logging.getLogger("maiasahi")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

posts_path = Path(".") / "maiasahi" / "content" / "post"
quiz_path = Path(".") / "maiasahi" / "content" / "quiz"
URL = "https://asahi.com"

lower_limit = 500
upper_limit = 1500


def get_free_articles() -> list[str]:
    """
    Scans the div elements with classes 'p-topNews__listItem' and 'p-topNews2__listItem'
    on the page 'https://asahi.com'. Looks for the first div that does not contain a
    figure element with class 'c-icon c-icon--keyGold'. Returns the href value of the
    first a element within a div with class 'c-articleModule' inside the found div.

    Returns
    -------
        list[str]: href value if a suitable element is found.
    """
    response = requests.get(URL, timeout=500)
    response.raise_for_status()  # Raises a HTTPError for bad responses (4xx and 5xx)
    soup = BeautifulSoup(response.content, "html.parser")

    # Combine both types of divs into one list for scanning
    div_elements = soup.find_all("div", class_="p-topNews__listItem")

    results = []

    for div_element in div_elements:
        key_gold_figure = div_element.find("figure", class_="c-icon c-icon--keyGold")
        if key_gold_figure is None:
            article_module_div = div_element.find("div", class_="c-articleModule")
            if article_module_div is not None:
                a_element = article_module_div.find("a")
                if a_element is not None and a_element.has_attr("href"):
                    results.append(a_element["href"])

    return results


def extract_articles(urls: list[str]) -> dict[str, str]:
    """Extract contents from a list of urls

    Parameters
    ----------
    urls
        A list of urls.

    Returns
    -------
        A dict of contents extracted from the url.
    """

    for url in urls:
        full_url = URL + url

        article_content = extract_article_content(full_url)
        article_length = len(article_content["article"])
        if lower_limit < article_length < upper_limit:
            return article_content

    raise ValueError("Article not found!")


def extract_article_content(url: str) -> dict[str, Any]:
    """
    Extracts specific content from a given article webpage.

    Parameters:
    url (str): The URL of the article webpage.

    Returns:
    dict: A dictionary containing the following keys and their respective values:
        - 'title'    : Content of the h1 tag.
        - 'figure'   : URL of the image within the figure tag.
        - 'caption'  : Content of the figcaption tag.
        - 'article'  : Text content of all but the last p tag within a div with class
                       'nfyQp'. Paragraphs are separated by two newlines.
    """

    # Dictionary to store results
    result = {
        "title": None,
        "figure": None,
        "caption": None,
        "article": None,
        "link": url,
    }

    # Fetch HTML content
    response = requests.get(url, timeout=500)
    if response.status_code != 200:
        raise ValueError("Error: Couldn't fetch the URL")

    # Parse HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract title
    title_div = soup.find("div", {"class": "y_Qv3"})
    if title_div:
        title = title_div.find("h1")
        if title:
            title = cast(Tag, title)
            result["title"] = title.text.strip()

    # Extract figure URL
    figure = soup.find("figure")
    if figure:
        img = cast(Tag, figure.find("img"))
        if img and "srcset" in img.attrs:
            result["figure"] = "https:" + img["srcset"][0]

    # Extract caption
    caption = soup.find("figcaption")
    if caption:
        result["caption"] = caption.text

    # Extract article content
    div = soup.find("div", {"class": "nfyQp"})
    if div:
        div = cast(Tag, div)
        p_tags = div.find_all("p")
        article_content = []
        for p in p_tags[:-1]:  # Exclude the last p tag
            article_content.append(p.text)
        result["article"] = "\n\n".join(article_content).replace("\u3000", "")
        if result["article"]:
            result["article"] = re.sub(r"\n+", "\n\n", result["article"])

    if not result:
        raise ValueError("Error: Couldn't extract content from the URL")
    return result


def render(content: dict[str, str]) -> str:
    """Renders the jinja template with content.

    Parameters
    ----------
    content
        A dict with content.

    Returns
    -------
        The result after rendering the template.
    """
    env = Environment(loader=PackageLoader("maiasahi", "."))
    template = env.get_template("article.tpl")
    return template.render(content)


async def save_quiz(quiz: dict, formatted_date: str):
    """Saves the quiz content to a file.

    Parameters
    ----------
    quiz
        The quiz content.
    """
    async with aiofiles.open(
        quiz_path / f"{formatted_date}.json", "w", encoding="utf-8"
    ) as f:
        logger.info("Saving quiz as a json file...")
        await f.write(json.dumps(quiz, ensure_ascii=False, indent=2))


async def save_post(article_content: dict):
    """Saves the post content to a file.

    Parameters
    ----------
    article_md
        The post content.
    """
    formatted_date = article_content["date"]
    article_md = render(article_content)

    logger.info("Saving article as a post...")
    post_path = posts_path / f"{formatted_date}.md"

    async with aiofiles.open(post_path, "w", encoding="utf-8") as f:
        await f.write(article_md)

    logger.info("Post successfully saved at %s", str(posts_path))


async def add_article():
    free_article_urls = get_free_articles()

    if not free_article_urls:
        logger.info("Did not find any free articles on the home page!")
        logger.info("Looking for articles in subsections")
        section = random.choice(sections)
        url = get_links(section)
        article_content = extract_article_content(url)
    else:
        logger.info("Found %d free articles", len(free_article_urls))
        try:
            article_content = extract_articles(free_article_urls)
        except ValueError:
            logger.info("Looking for articles in subsections")
            section = random.choice(sections)
            url = get_links(section)
            article_content = extract_article_content(url)

    logger.info(
        "Successfully extracted content of article with title %s",
        article_content["title"],
    )

    article = article_content["article"].replace("\u3000", "")
    title = article_content["title"]

    logger.info("Furigana annotation with ChatGPT")

    annotation_results = await annotate_article(title, article)

    today = datetime.today()
    formatted_date = today.strftime("%Y-%m-%d")

    logger.info("Adding audio to article...")
    await add_audio_from_article(article, formatted_date)

    annotated_article = annotation_results["article"]

    logger.info("Successfully retrieved annotations from ChatGPT!")
    logger.info("%s", annotated_article[: min(30, len(annotated_article))])

    logger.info("Successfully retrieved slugs!")
    logger.info(annotation_results["title"])

    logger.info("Successfully retrieved vocabulary from ChatGPT!")
    logger.info("Successfully retrieved grammar from ChatGPT!")
    logger.info("Successfully retrieved quiz from ChatGPT!")

    annotation_results["date"] = formatted_date
    annotation_results["figure"] = article_content["figure"]
    annotation_results["caption"] = article_content["caption"]
    annotation_results["link"] = article_content["link"]

    await save_post(annotation_results)
    await save_quiz(annotation_results["quiz"], formatted_date)


def main():
    asyncio.run(add_article())
