from pathlib import Path
import random

from .gcloud import gcloud_text_to_speech, names


pattern = r"\[Link to the original article\]\((.*?)\)"
audio_dir = Path(".") / "maiasahi" / "content" / "audio"


def add_audio_from_article(article_content: str, save_dir=str) -> None:
    """Add audio from article, using Google Cloud Text-to-Speech

    Args:
        article_content (str): Article content
    """
    save_dir = audio_dir / save_dir
    save_dir.mkdir(exist_ok=True)

    name = random.choice(names)

    for idx, para in enumerate(article_content.split("\n\n")):
        print(f"Saving {idx}.ogg")
        gcloud_text_to_speech(para, save_dir / f"p{idx}.ogg", name=name)
