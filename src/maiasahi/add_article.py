from datetime import datetime
import logging
import os
from pathlib import Path
import re

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from jinja2 import Environment, PackageLoader
import openai
import requests

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

logger = logging.getLogger("maiasahi")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

posts_path = Path(".") / "maiasahi" / "content" / "post"
URL = "https://asahi.com"

lower_limit = 200
upper_limit = 1000


def get_free_articles() -> list[str]:
    """
    Scans the div elements with classes 'p-topNews__listItem' and 'p-topNews2__listItem'
    on the page 'https://asahi.com'. Looks for the first div that does not contain a
    figure element with class 'c-icon c-icon--keyGold'. Returns the href value of the
    first a element within a div with class 'c-articleModule' inside the found div.

    Returns:
        str: href value if a suitable element is found.
        None: if no such element can be found.
    """
    response = requests.get(URL, timeout=500)
    response.raise_for_status()  # Raises a HTTPError for bad responses (4xx and 5xx)
    soup = BeautifulSoup(response.content, "html.parser")

    # Combine both types of divs into one list for scanning
    div_elements = soup.find_all("div", class_="p-topNews__listItem") + soup.find_all(
        "div", class_="p-topNews2__listItem"
    )

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
        _description_

    Returns
    -------
        _description_
    """
    articles_over_length = []

    for url in urls:
        full_url = URL + url

        article_content = extract_article_content(full_url)
        article_length = len(article_content["article"])
        if article_length < upper_limit:
            if article_length > lower_limit:
                return article_content
            else:
                continue

        articles_over_length.append(article_content)

    # If no articles has been found:
    for article_content in articles_over_length:
        article = article_content["article"]

        paragraphs = re.split(r"\n+", article.strip())
        para_idx = 0
        length = 0

        while length < upper_limit and para_idx < len(paragraphs):
            length += len(paragraphs[para_idx])
            para_idx += 1

        article_content["article"] = "\n\n".join(paragraphs[:para_idx])

        return article_content

    raise ValueError("Article not found!")


def extract_article_content(url: str) -> dict[str, str]:
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
        return "Error: Couldn't fetch the URL"

    # Parse HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract title
    title = soup.find("div", {"class": "y_Qv3"}).find("h1")
    if title:
        result["title"] = title.text.strip()

    # Extract figure URL
    figure = soup.find("figure")
    if figure:
        img = figure.find("img")
        if img and "src" in img.attrs:
            result["figure"] = "https:" + img["src"]

    # Extract caption
    caption = soup.find("figcaption")
    if caption:
        result["caption"] = caption.text

    # Extract article content
    div = soup.find("div", {"class": "nfyQp"})
    if div:
        p_tags = div.find_all("p")
        article_content = []
        for p in p_tags[:-1]:  # Exclude the last p tag
            article_content.append(p.text)
        result["article"] = "\n\n".join(article_content).replace("\u3000", "")
        result["article"] = re.sub(r"\n+", "\n\n", result["article"])

    return result


def annotate_with_chatgpt(article: str) -> str:
    """Annotate pronunciation with ChatGPT.

    Parameters
    ----------
    article
        The content of the article.
    """
    prompt = (
        "For each of the above paragraphs, annotate the pronunciation of all "
        + "kanji with furigana in html <ruby> tags for accessibility"
    )
    content = f"{article}\n\n{prompt}"
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": content}]
    )
    response = completion.choices[0].message.content

    if "<ruby>" in response:
        return response

    new_prompt = f"For each of the paragraphs below, convert the furigana in parentheses into HTML <ruby> tags for accessibility\n\n{response}"

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": new_prompt}]
    )

    return completion.choices[0].message.content


def annotate_with_chatgpt_with_retry(article: str, retries: int = 3) -> str:
    """Annotate pronunciation with ChatGPT.

    Parameters
    ----------
    article
        The content of the article.
    """

    for _ in range(retries):
        annotated_content = annotate_with_chatgpt(article)
        if "<ruby>" in annotated_content:
            return annotated_content

    raise ValueError(f"ChatGPT returned no annotations after {retries} retries!")


def slug_with_chatgpt(title: str) -> str:
    """Translates the title with ChatGPT and convert to a slug.

    Parameters
    ----------
    title
        The title of the article.
    """
    prompt = f"""{title}
    
    Translate the above sentence from Japanese into English.
    """

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )

    translation = completion.choices[0].message.content
    slug = sentence_to_slug(translation)

    return slug


def vocabulary_with_chatgpt(article: str) -> str:
    """Find a list of vocabulary in the article with ChatGPT.

    Parameters
    ----------
    article
        The article in string form

    Returns
    -------
        A list of vocabulary in markdown.
    """
    prompt = f"""
    {article}

    Find 30 words at JLPT N3 N2 and N1 levels in the article above. Exclude proper nouns. Convert each word to its dictionary form. Prioritize verbs and adjectives. List in markdown table with the following columns: 
    1. Word: write each word in dictionary form with furigana in parentheses next to it
    2. JLPT Level: whether they are JLPT N5, N4, N3, N2, or N1 words
    3. Part of speech: for adjectives, be specific about whether they are い-adjectives or な-adjectives. For verbs, be specific about whether they are ichidan, godan, or irregular verbs
    4. Meaning: write in lower case.
    """
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content


def grammar_with_chatgpt(article: str) -> str:
    """Find a list of vocabulary in the article with ChatGPT.

    Parameters
    ----------
    article
        The article in string form

    Returns
    -------
        Explanation of a complex sentence in markdown.
    """
    prompt = f"""
    {article}

    In the above article, select 3 sentences that are difficult to understand. For each sentence, do the following:

    1. explain grammatical points
    2. explain the structure of the sentence

    Organize the results in markdown
    """
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content


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


def sentence_to_slug(title):
    # Convert to lowercase
    title = title.lower()

    # Remove any special characters or punctuation, and replace spaces with hyphens
    slug = re.sub(r"[^a-z0-9]+", "-", title).strip("-")

    return slug


def add_article():
    free_article_urls = get_free_articles()

    if not free_article_urls:
        raise ValueError("Cannot locate any free article!")

    logger.info("Found %d free articles", len(free_article_urls))

    article_content = extract_articles(free_article_urls)

    logger.info(
        "Successfully extracted content of article with title %s",
        article_content["title"],
    )

    article = article_content["article"].replace("\u3000", "")

    logger.info("Furigana annotation with ChatGPT")
    annotated_content = annotate_with_chatgpt(article)
    logger.info("Successfully retrieved annotations from ChatGPT!")
    logger.info("%s", annotated_content[: min(30, len(annotated_content))])

    paragraphs = re.split(r"\n+", annotated_content)
    html_content = "\n".join([f"<p>{paragraph}</p>" for paragraph in paragraphs])

    slug = slug_with_chatgpt(article_content["title"])

    logger.info("Successfully retrieved slugs!")
    logger.info(slug)

    article_content["vocabulary"] = vocabulary_with_chatgpt(article)
    logger.info("Successfully retrieved vocabulary from ChatGPT!")

    article_content["grammar"] = grammar_with_chatgpt(article)
    logger.info("Successfully retrieved grammar from ChatGPT!")

    article_content["article"] = html_content

    today = datetime.today()
    formatted_date = today.strftime("%Y-%m-%d")

    article_content["date"] = formatted_date
    article_content["slug"] = slug

    article = render(article_content)

    logger.info("Saving article as a post...")
    post_path = posts_path / f"{formatted_date}.md"

    with open(post_path, "w", encoding="utf-8") as f:
        f.write(article)

    logger.info("Post successfully saved at %s", str(posts_path))
