from maiasahi.add_article import (
    annotate_by_paragraph,
    slug_with_chatgpt,
    annotate_with_chatgpt,
)

article = """
    ラグビーワールドカップ（W杯）の1次リーグD組で、日本は8日、アルゼンチンと対戦し、27―39で敗れた。通算成績は2勝2敗でD組3位となり、2大会連続の決勝トーナメント進出はならなかった。

    分かっちゃいるけど、止められない。そう表現するしかないほど、アルゼンチンの圧力は別格だった。勝負どころの接点で日本は負けた。タックルでラックでモールで、前進を許した。

    前半は、何とかこらえていた。開始早々に先制トライを喫したが、トライを奪い返して食い下がった。ただし、一つひとつのプレーが終わるたび、アルゼンチンにエネルギーを削られていった。

    後半2分が、象徴的だ。日本の反則で、時計が止まった。赤と白のジャージーを着た選手の多くが、肩で呼吸をしている。つい数分前まで、ハーフタイムで息を整えたとは思えないほど、疲労の色が濃かった。

    アルゼンチンがやったことは、最後まで単純だった。ハイボールを絶妙な位置に蹴り込み陣地回復。敵陣に入ると、局面を重ねてプレッシャーをかけ続ける。後半6分、28分に許した失トライは、直線的に何度も攻められた末、防御網に穴があいた結果だ。

    前回W杯の再現、いや、それ以上の結果をめざし、けが人が続出するほどの厳しい合宿にも耐え、相手の分析も念入りにしてきた。試合後、FWリーチはすがすがしい表情で言った。「全力を尽くした。準備も良かった。でも相手の方が強かった。それがラグビーです」

    過去2度の4強入りを経験している相手に、ガチンコでぶつかった。悔しい敗戦の積み重ねが、日本ラグビーの歴史をつくる。「次に託したい」とFW稲垣。敗れはしたが、価値ある一戦だった。（ナント=松本龍三郎）
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
