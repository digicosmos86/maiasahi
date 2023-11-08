from maiasahi.add_article import annotate_by_paragraph

from maiasahi.gpt import (
    paragraph_with_chatgpt,
    sentence_to_slug,
    quiz_with_chatgpt,
    slug_with_chatgpt,
)

article = """ビートルズの「最後の曲」とされる「ナウ・アンド・ゼン」が日本時間2日午後11時にデジタル配信で発売された。3日にはアナログ盤も発売され、ミュージックビデオも公開される予定。1970年解散のビートルズの名義で新たな曲が発売されるのは27年ぶりとなる。

　「ナウ・アンド・ゼン」（Now　And　Then、『時々』の意）は「時々君が恋しくなる」といった詞で、大切な人への断ち切れない思いを吐露する曲。62年のデビュー曲「ラヴ・ミー・ドゥ」との両A面での発売となった。

　ジョン・レノンが生前に残したデモ音源をもとに、最新技術でレノンの声をクリアによみがえらせ、現在のポール・マッカートニーさんやリンゴ・スターさんの演奏、ジョージ・ハリソン（2001年死去）が95年に録音したギターなどと合わせた「新曲」として、発売前から話題を呼んでいた。（野城千穂）
    """


def test_chatgpt():
    title = "「世界ふしぎ発見！」レギュラー放送終了へ　草野さん「天職だった」"

    slug = slug_with_chatgpt(title)

    assert slug.lower() == slug
    assert "\n" not in slug
    assert " " not in slug


def test_annotate_by_paragraph():
    annotated_content = annotate_by_paragraph(article)
    print(annotated_content)


def test_quiz_with_chatgpt():
    quiz = quiz_with_chatgpt(article)
    print(quiz)
