from pathlib import Path
import random

from .gcloud import gcloud_text_to_speech, names


pattern = r"\[Link to the original article\]\((.*?)\)"
audio_dir = "audio"


def add_audio_from_article(article_content: str, save_dir=str) -> None:
    """Add audio from article, using Google Cloud Text-to-Speech

    Args:
        article_content (str): Article content
    """
    save_dir = f"{audio_dir}/{save_dir}"

    name = random.choice(names)

    for idx, para in enumerate(article_content.split("\n\n")):
        print(f"Saving {idx}.mp3")
        gcloud_text_to_speech(para, f"{save_dir}/p{idx}.mp3", name=name)


if __name__ == "__main__":
    pass
    # import re
    # from add_article import extract_article_content

    # posts_dir = Path(".") / "maiasahi" / "content" / "post"

    # posts = sorted(posts_dir.glob("*.md"))
    # pattern = r'\[Link to the original article\]\((.*?)\)'

    # for post in posts:
    #     print(f"Adding audio for {post}")
    #     with open(post, "r") as f:
    #         text = f.read()

    #     match = re.search(pattern, text)
    #     if match:
    #         url = match.group(1)
    #         print(url)
    #         article = extract_article_content(url)["article"]
    #     else:
    #         raise ValueError(f"Cannot find url for {post}")

    #     add_audio_from_article(article, post.stem)
