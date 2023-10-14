import os
from dotenv import load_dotenv

from maiasahi.gcloud import gcloud_text_to_speech
from maiasahi.add_article import render

load_dotenv()


def test_enviorn():
    assert os.getenv("GOOGLE_APPLICATION_CREDENTIALS") is not None
    assert os.getenv("OPENAI_API_KEY") is not None
    assert os.getenv("OPENAI_API_KEY")[:2] == "sk"


def test_gcloud_text_to_speech():
    text = "Hello, World!"

    gcloud_text_to_speech(text, "output.ogg")


def test_render():
    content = {
        "title": "this is a title",
        "slug": "this-is-a-slug",
        "date": "2021-01-01",
        "link": "https://www.google.com",
        "article": "this is an article",
        "vocabulary": "this is a vocabulary",
        "summary": "this is a summary",
    }

    render(content)
