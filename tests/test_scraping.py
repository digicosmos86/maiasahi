from maiasahi.add_article import get_free_articles, extract_articles

def test_extraction():

    urls = get_free_articles()
    assert urls is not None

    print(len(urls))

    article = extract_articles(urls)

    print("title: ", article["title"])
    print(article["article"])
    print(article["figure"])
    print(article["caption"])
