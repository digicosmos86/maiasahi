from maiasahi.add_article import slug_with_chatgpt


def test_chatgpt():
    title = "「世界ふしぎ発見！」レギュラー放送終了へ　草野さん「天職だった」"

    slug = slug_with_chatgpt(title)

    assert slug.lower() == slug
