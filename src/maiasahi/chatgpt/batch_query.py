import asyncio
import json

from typing import cast

from .clients import client
from .batch_requests import create_all_requests
from .utils import (
    create_request_file,
    find_id,
    markdown_table_linker,
    requests_to_dict,
    split_responses,
    sentence_to_slug,
)

MAX_RETRIES = 3


def retrieve_content(res: dict) -> str:
    """Retrieve the content from a response."""
    return res["response"]["body"]["choices"][0]["message"]["content"]


def retrieve(responses: list[dict], id: str) -> str:
    """Retrieve the content from a response."""
    res = find_id(responses, id)
    return retrieve_content(res)


async def make_batch_request(requests: list[dict]) -> list[dict]:
    """Make a batch request and wait asynchronously until it's finished."""
    request_file = create_request_file(requests)
    batch_file = client.files.create(file=request_file, purpose="batch")

    input_file_id = batch_file.id

    batch = client.batches.create(
        input_file_id=input_file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={"description": "annotation requests"},
    )
    batch_id = batch.id

    for _ in range(24 * 60 * 60 // 3):
        batch_result = client.batches.retrieve(batch_id=batch_id)
        if batch_result.status == "completed":
            break
        await asyncio.sleep(3)

    if batch_result.status != "completed":
        raise RuntimeError("Batch request did not complete successfully.")

    output_file_id = cast(str, batch_result.output_file_id)
    response_file = client.files.content(file_id=output_file_id)

    result = [json.loads(line) for line in response_file.iter_lines()]

    return result


def responses_to_dict(responses: list[dict]) -> dict:
    """Converts a list of responses to a dictionary for templating."""
    paragraphs = [
        (int(res["custom_id"].replace("annotate-p", "")), retrieve_content(res))
        for res in responses
        if "annotate-p" in res["custom_id"]
    ]

    sorted_paragraphs = sorted(paragraphs, key=lambda x: x[0])
    article = "\n\n".join([p[1] for p in sorted_paragraphs])

    slug = sentence_to_slug(retrieve(responses, "title"))
    vocabulary = markdown_table_linker(retrieve(responses, "vocabulary"))
    grammar = retrieve(responses, "grammar")
    quiz = json.loads(retrieve(responses, "quiz"))

    return {
        "slug": slug,
        "article": article,
        "vocabulary": vocabulary,
        "grammar": grammar,
        "quiz": quiz,
    }


async def annotate_article(title: str, article: str) -> dict:
    """Annotate an article with ChatGPT."""
    requests = create_all_requests(title, article)
    requests_dict = requests_to_dict(requests)
    responses = await make_batch_request(requests)

    success, errors = split_responses(responses)

    retries = 0

    while len(errors) > 0 and retries < MAX_RETRIES:
        print(f"Retrying {len(errors)} failed requests...")
        new_requests = [requests_dict[req["custom_id"]] for req in errors]
        new_responses = await make_batch_request(new_requests)
        new_success, new_errors = split_responses(new_responses)
        success.extend(new_success)
        errors = new_errors

    result = responses_to_dict(success)
    result["title"] = title

    return result
