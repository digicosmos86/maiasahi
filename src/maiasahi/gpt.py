import json
import re
import os
import urllib.parse

import openai
from dotenv import load_dotenv
from retry import retry

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

MODEL = "gpt-3.5-turbo-0125"


@retry(tries=5, delay=2)
def paragraph_with_chatgpt(paragraph: str):
    """Annotate a single paragraph with ChatGPT."""
    system = """You are an app that annotates furigana using <ruby> and <rt> tags. For example, if the paragraph is <p>ビートルズの「最後の曲」とされる「ナウ・アンド・ゼン」が日本時間2日午後11時にデジタル配信で発売された。</p>

 Then the response should be <p><ruby>ビートルズ<rt>びーとるず</rt></ruby>の「<ruby>最後<rt>さいご</rt></ruby>の<ruby>曲<rt>きょく</rt></ruby>」とされる「<ruby>ナウ・アンド・ゼン<rt>なう・あんど・ぜん</rt></ruby>」が<ruby>日本<rt>にほん</rt></ruby><ruby>時間<rt>じかん</rt></ruby>2<ruby>日<rt>にち</rt></ruby><ruby>午後<rt>ごご</rt></ruby>11<ruby>時<rt>じ</rt></ruby>に<ruby>デジタル<rt>でじたる</rt></ruby><ruby>配信<rt>はいしん</rt></ruby>で<ruby>発売<rt>はつばい</rt></ruby>された。</p>"""

    prompt = f"Now annotate this paragraph: <p>{paragraph}</p>. Your response should be HTML with matching <ruby> and <rt> tags for all words and phrases."

    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return completion.choices[0].message.content


@retry(tries=5, delay=2)
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
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    translation = completion.choices[0].message.content
    slug = sentence_to_slug(translation)

    return slug


def markdown_table_linker(md_table: str) -> str:
    # Split the table by lines
    lines = md_table.strip().split("\n")

    # For header and separator rows, keep as is.
    new_lines = [lines[0], lines[1]]

    for line in lines[2:]:
        # Split the line into columns
        cols = line.strip().split("|")

        word = cols[1].strip()
        rest = None

        if "（" in word:
            idx = word.index("（")
            rest = word[idx:].strip()
            word = word[:idx].strip()
        elif "(" in word:
            idx = word.index("(")
            rest = word[idx:].strip()
            word = word[:idx].strip()

        # URL-encode the first column's content (which is usually the second element after split)
        encoded_str = urllib.parse.quote_plus(word)
        hyperlink = f"[{word}](https://jisho.org/search/{encoded_str})"

        # Replace the first column's content with the hyperlink
        cols[1] = hyperlink + (f" {rest}" if rest else "")

        # Re-join the columns and add to new_lines
        new_lines.append("|".join(cols))

    # Re-join the lines and return
    return "\n".join(new_lines)


def sentence_to_slug(title):
    # Convert to lowercase
    title = title.lower()

    # Remove any special characters or punctuation, and replace spaces with hyphens
    slug = re.sub(r"[^a-z0-9]+", "-", title).strip("-")

    return slug


@retry(tries=5, delay=2)
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
    system = "You are an app that helps intermediate and advanced Japanese learners learn intermediate and advanced level vocabulary."
    prompt = f"""From the article below, find 30 intermediate and advanced words that are at JLPT N1, N2, and N3 levels.  Focus on verbs, adjectives, and adverbs. Make sure to combine all results in one markdown table with the following columns:

1. Word: write each word in dictionary form with furigana in parentheses next to it
2. JLPT Level: whether they are JLPT N5, N4, N3, N2, or N1 words
3. Part of speech: for adjectives, be specific about whether they are い-adjectives or な-adjectives. For verbs, be specific about whether they are ichidan, godan, or irregular verbs
4. Meaning: write in lower case.

<article>
{article}
</article>
    """
    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    result = completion.choices[0].message.content

    return markdown_table_linker(result)


@retry(tries=5, delay=2)
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
    system = "You are an app that helps intermediate and advanced Japanese learners learn intermediate and advanced level grammar."
    prompt = f"""
    {article}

    In the above article, select 3 sentences that are difficult to understand. For each sentence, do the following:

    1. explain grammatical points
    2. explain the structure of the sentence

    Your response should be the markdown only. Do not put it in a code block.
    """
    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return completion.choices[0].message.content


@retry(tries=5, delay=2)
def quiz_with_chatgpt(article: str) -> str:
    """Generate a quiz with ChatGPT.

    Parameters
    ----------
    article
        The article in string form

    Returns
    -------
        A list of vocabulary in markdown.
    """
    system = "You are a Japanese tutoring app teaching intermediate level adult students. You are designing a quiz to test reading comprehension of Japanese articles. Do not format your answer in Markdown."
    prompt = f"""The quiz has 5 questions based on an article below. The questions should test the comprehension of the article. Each question should have one correct answer and three incorrect answers. The incorrect answers cannot be too obviously wrong, and the order of the options should be random. One good examples for the question is:  この記事で語られている事件の詳細は何ですか？ However, you cannot use the same question in the example. 

Here's the article:

{article}

I want the quiz as an array of JSON objects with the following field: 
1. question: the question itself,
2. options: an array of 4 options,
3. answer: the index of the correct answer in the options array
4. explanation, which is an explanation of the correct answer.

Your response should be nothing but the array. Do not format your answer in Markdown.
"""
    completion = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    json_obj = json.loads(completion.choices[0].message.content)

    return json_obj
