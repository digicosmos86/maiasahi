from maiasahi.add_article import (
    annotate_by_paragraph,
    slug_with_chatgpt,
    annotate_with_chatgpt,
)

article = """
    改正案は、全国で相次ぐ置き去りによる子どもの死亡事故を受け、同県議団が4日、県議会に提出した。6日の県議会福祉保健医療委員会で自民、公明両党県議団の賛成により可決され、13日の議会最終日に採決される予定だった。

    県内では保護者らの反発が高まり、さいたま市PTA協議会（市P協）は6日に反対の署名活動を始めた。（西田有里）
    """


def test_chatgpt():
    title = "「世界ふしぎ発見！」レギュラー放送終了へ　草野さん「天職だった」"

    slug = slug_with_chatgpt(title)

    assert slug.lower() == slug
    assert "\n" not in slug
    assert " " not in slug


def test_pronunciation():
    annotated_content = annotate_with_chatgpt(article)
    print(annotated_content)


def test_annotate_by_paragraph():
    annotated_content = annotate_by_paragraph(article)
    print(annotated_content)
