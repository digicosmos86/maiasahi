from maiasahi.add_article import (
    get_free_articles,
    extract_articles,
    markdown_table_linker,
)


def test_extraction():
    urls = get_free_articles()
    assert urls is not None

    print(len(urls))

    article = extract_articles(urls)

    print("title: ", article["title"])
    print(article["article"])
    print(article["figure"])
    print(article["caption"])


def test_markdown_linker():
    markdown_table = """
| Word                            | JLPT Level  | Part of Speech   | Meaning                     |
| ------------------------------- | ----------- | ---------------- | --------------------------- |
|[続く](https://jisho.org/search/%E7%B6%9A%E3%81%8F)(つづく)| N3          | verb (godan)     | to continue                 |
|[発表する](https://jisho.org/search/%E7%99%BA%E8%A1%A8%E3%81%99%E3%82%8B)(はっぴょうする)| N3          | verb (irregular) | to announce                 |
|[終了する](https://jisho.org/search/%E7%B5%82%E4%BA%86%E3%81%99%E3%82%8B)(しゅうりょうする)| N3          | verb (irregular) | to end                      |
|[特番](https://jisho.org/search/%E7%89%B9%E7%95%AA)(とくばん)| N3          | noun             | special program             |
|[解き明かす](https://jisho.org/search/%E8%A7%A3%E3%81%8D%E6%98%8E%E3%81%8B%E3%81%99)(ときあかす)| N3          | verb (godan)     | to solve/reveal             |
|[放送する](https://jisho.org/search/%E6%94%BE%E9%80%81%E3%81%99%E3%82%8B)(ほうそうする)| N3          | verb (irregular) | to broadcast                |
|[出演する](https://jisho.org/search/%E5%87%BA%E6%BC%94%E3%81%99%E3%82%8B)(しゅつえんする)| N3          | verb (irregular) | to appear (on stage/screen) |
|[司会を務める](https://jisho.org/search/%E5%8F%B8%E4%BC%9A%E3%82%92%E5%8B%99%E3%82%81%E3%82%8B)(しかいをつとめる)| N3          | verb phrase      | to serve as a host          |
|[連続する](https://jisho.org/search/%E9%80%A3%E7%B6%9A%E3%81%99%E3%82%8B)(れんぞくする)| N3          | verb (irregular) | to occur consecutively      |
|[大きい](https://jisho.org/search/%E5%A4%A7%E3%81%8D%E3%81%84)(おおきい)| N4          | い-adjective     | big                         |
|[出来る](https://jisho.org/search/%E5%87%BA%E6%9D%A5%E3%82%8B)(できる)| N4          | verb (ichidan)   | can/do/make                 |
|[見る](https://jisho.org/search/%E8%A6%8B%E3%82%8B)(みる)| N4          | verb (ichidan)   | to watch                    |
|[言う](https://jisho.org/search/%E8%A8%80%E3%81%86)(いう)| N4          | verb (godan)     | to say                      |
|[寄せる](https://jisho.org/search/%E5%AF%84%E3%81%9B%E3%82%8B)(よせる)| N4          | verb (ichidan)   | to send                     |
|[覚える](https://jisho.org/search/%E8%A6%9A%E3%81%88%E3%82%8B)(おぼえる)| N4          | verb (ichidan)   | to remember                 |
|[思う](https://jisho.org/search/%E6%80%9D%E3%81%86)(おもう)| N4          | verb (godan)     | to think                    |
|[務める](https://jisho.org/search/%E5%8B%99%E3%82%81%E3%82%8B)(つとめる)| N4          | verb (ichidan)   | to serve                    |
|[楽しむ](https://jisho.org/search/%E6%A5%BD%E3%81%97%E3%82%80)(たのしむ)| N4          | verb (godan)     | to enjoy                    |
|[捌く](https://jisho.org/search/%E6%8D%8C%E3%81%8F)(さばく)| N4          | verb (godan)     | to deal with                |
|[入れる](https://jisho.org/search/%E5%85%A5%E3%82%8C%E3%82%8B)(いれる)| N4          | verb (ichidan)   | to put in                   |
|[集める](https://jisho.org/search/%E9%9B%86%E3%82%81%E3%82%8B)(あつめる)| N4          | verb (ichidan)   | to collect                  |
|[横浜](https://jisho.org/search/%E6%A8%AA%E6%B5%9C)(よこはま)| Proper Noun | noun             | Yokohama (city in Japan)    |
|[重圧](https://jisho.org/search/%E9%87%8D%E5%9C%A7)(じゅうあつ)| N3          | noun             | pressure                    |
|[慣れる](https://jisho.org/search/%E6%85%A3%E3%82%8C%E3%82%8B)(なれる)| N4          | verb (ichidan)   | to get used to              |
|[覚える](https://jisho.org/search/%E8%A6%9A%E3%81%88%E3%82%8B)(おぼえる)| N4          | verb (ichidan)   | to remember                 |
|[半年](https://jisho.org/search/%E5%8D%8A%E5%B9%B4)(はんとし)| N4          | noun             | half a year                 |
|[入れる](https://jisho.org/search/%E5%85%A5%E3%82%8C%E3%82%8B)(いれる)| N4          | verb (ichidan)   | to put in                   |
|[気合](https://jisho.org/search/%E6%B0%97%E5%90%88)(きあい)| N4          | noun             | fighting spirit             |
|[臨む](https://jisho.org/search/%E8%87%A8%E3%82%80)(のぞむ)| N4          | verb (godan)     | to face/approach            |
|[若手](https://jisho.org/search/%E8%8B%A5%E6%89%8B)(わかて)| N4          | noun             | young person                |
|[お年寄り](https://jisho.org/search/%E3%81%8A%E5%B9%B4%E5%AF%84%E3%82%8A)(おとしより)| N4          | noun             | elderly person              |
|[豪華](https://jisho.org/search/%E8%B1%AA%E8%8F%AF)(ごうか)| N3          | な-adjective     | gorgeous/amazing            |
"""

    result = markdown_table_linker(markdown_table)
    print(result)
