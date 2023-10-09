from maiasahi.add_article import (
    annotate_by_paragraph,
    slug_with_chatgpt,
    annotate_with_chatgpt,
)

article = """
    大阪市生野区桃谷2丁目の路上で8日午後6時10分ごろ、だんじりを先頭で引いていた職業不詳、佐古吉隆さん（52）=大阪市生野区=が、だんじりとガードレールの間に挟まれた。佐古さんは病院に搬送されたが、9日朝に出血性ショックで死亡した。約30人がだんじりを引いていたが、ほかにけが人はなかった。

    　生野署によると、だんじりが道路を左折する際、停止しようとしたがしきれずにガードレールに衝突したとみられる。地区の祭りに備えた練習だった。事故当時は雨が降っており、路面がぬれていたという。署は当時の詳しい状況や事故原因を調べている。
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
