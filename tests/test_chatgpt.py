from maiasahi.add_article import (
    annotate_by_paragraph,
    slug_with_chatgpt,
    annotate_with_chatgpt,
)

article = """
    NHKは10日、2024～26年度の中期経営計画案を発表した。26年度にAMの「ラジオ第1」と「第2」から1波を削減し、AM1波、FM1波とすることや、27年度までに1千億円の支出削減を行う方針を明記した。経営委員会が同日、大筋で了承した。11日から意見募集し、年明けに正式決定する。

    語学番組など人気番組があるAMラジオを1波削減することについて、稲葉延雄会長はこの日の会見で「消費者の利便性を損なわないようにしたい」と述べた。

    中計案では、今年10月の受信料値下げなどに伴う収入減を踏まえ、23年度の6720億円の事業支出を段階的に縮小し、27年度に5770億円にする方針も明記。24～26年度のNHK予算は赤字収支が見込まれるため、「還元目的積立金」で補い、27年度に収支均衡を目指すという。森下俊三経営委員長は報道陣に「受信料の値下げは非常に大きく、1千億円の財政改善をする挑戦的な計画になった」と語った。
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
