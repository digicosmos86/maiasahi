import pytest

from maiasahi.chatgpt.batch_requests import create_batch_request, create_all_requests
from maiasahi.chatgpt.batch_query import (
    make_batch_request,
    retrieve_content,
    responses_to_dict,
)
from maiasahi.chatgpt.utils import create_request_file

title = "「世界ふしぎ発見！」レギュラー放送終了へ　草野さん「天職だった」"
article = """ビートルズの「最後の曲」とされる「ナウ・アンド・ゼン」が日本時間2日午後11時にデジタル配信で発売された。3日にはアナログ盤も発売され、ミュージックビデオも公開される予定。1970年解散のビートルズの名義で新たな曲が発売されるのは27年ぶりとなる。

　「ナウ・アンド・ゼン」（Now　And　Then、『時々』の意）は「時々君が恋しくなる」といった詞で、大切な人への断ち切れない思いを吐露する曲。62年のデビュー曲「ラヴ・ミー・ドゥ」との両A面での発売となった。

　ジョン・レノンが生前に残したデモ音源をもとに、最新技術でレノンの声をクリアによみがえらせ、現在のポール・マッカートニーさんやリンゴ・スターさんの演奏、ジョージ・ハリソン（2001年死去）が95年に録音したギターなどと合わせた「新曲」として、発売前から話題を呼んでいた。（野城千穂）
    """


def test_create_batch_request():
    id = "test-id"
    system = "System message"
    user = "User message"

    request = create_batch_request(id, system, user)

    assert request["custom_id"] == id
    assert request["method"] == "POST"
    assert request["url"] == "/v1/chat/completions"
    assert request["body"]["model"] == "gpt-4o-mini-2024-07-18"
    assert request["body"]["messages"][0]["role"] == "system"
    assert request["body"]["messages"][0]["content"] == system
    assert request["body"]["messages"][1]["role"] == "user"
    assert request["body"]["messages"][1]["content"] == user
    assert request["body"]["temperature"] == 0.2


def test_create_all_requests():
    requests = create_all_requests(title, article)

    assert len(requests) == 7
    assert requests[0]["custom_id"] == "annotate-p0"
    assert requests[1]["custom_id"] == "annotate-p1"
    assert requests[2]["custom_id"] == "annotate-p2"
    assert requests[3]["custom_id"] == "title"
    assert requests[4]["custom_id"] == "vocabulary"
    assert requests[5]["custom_id"] == "grammar"
    assert requests[6]["custom_id"] == "quiz"


def test_create_request_file():
    requests = create_all_requests(title, article)[:2]

    request_file = create_request_file(requests)
    len(request_file.splitlines()) == 2


@pytest.mark.asyncio
async def test_make_batch_request():
    requests = create_all_requests(title, article)[:2]

    responses = await make_batch_request(requests)

    print(responses)

    assert len(responses) == 2
    assert "annotate-p0" in responses[0]["custom_id"]
    assert "<ruby>" in retrieve_content(responses[0])


@pytest.mark.asyncio
async def test_make_batch_request():
    requests = create_all_requests(title, article)[:2]

    responses = await make_batch_request(requests)

    assert len(responses) == 2
    assert "annotate-p0" in responses[0]["custom_id"]
    assert "<ruby>" in retrieve_content(responses[0])


@pytest.mark.asyncio
async def test_responses_to_dict():
    requests = create_all_requests(title, article)
    responses = await make_batch_request(requests)

    result = responses_to_dict(responses)

    assert "article" in result
