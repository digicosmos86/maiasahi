import json
import re
import urllib.parse

from typing import Callable


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


def requests_to_dict(requests: list[dict]) -> dict:
    """Converts a list of requests to a dictionary with the request IDs as keys."""
    return {req["custom_id"]: req for req in requests}


def create_request_file(requests: list[dict]) -> bytes:
    """Create a JSON file with the given requests."""
    return "\n".join([json.dumps(req, ensure_ascii=False) for req in requests]).encode(
        "utf-8"
    )


def find(requests: list[dict], func: Callable) -> dict | None:
    """Find a request by its ID."""
    result = next(filter(func, requests), None)
    return result


def find_id(requests: list[dict], id: str) -> dict:
    """Find a request by its ID."""
    result = find(requests, lambda req: req["custom_id"] == id)
    if result is None:
        raise ValueError(f"Request with ID '{id}' not found.")
    return result


def split_responses(responses: list[dict]) -> tuple[list[dict], list[dict]]:
    """Split responses into successful and failed."""
    success = []
    failed = []

    for res in responses:
        if res["error"] is None:
            success.append(res)
        else:
            failed.append(res)

    return success, failed
