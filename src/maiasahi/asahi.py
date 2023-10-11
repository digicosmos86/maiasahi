from bs4 import BeautifulSoup
import requests

sections = [
    "national",
    "business",
    "politics",
    "international",
    "sports",
    "tech_science",
    "culture",
    "life",
    "edu",
    "apital",
]


def get_links(section) -> list[str]:
    """From url extract a list of URLs.

    Args:
        url (str): The URL to the website

    Returns:
        list[str]: a list of URLs
    """

    url = f"https://asahi.com/{section}/"

    response = requests.get(url, timeout=200)

    if response.status_code != 200:
        raise ValueError(f"HTTP failed with code {response.status_code}")

    html_content = response.text
    soup = BeautifulSoup(html_content, features="html.parser")

    uls = soup.find_all("ul", "List")

    if not uls:
        raise ValueError(f"Could not find any article on page {url}")

    for ul in uls:
        lis = ul.find_all("li", class_="Fst") + ul.find_all("li", class_="")

        if not lis:
            continue

        for li in lis:
            a_link = li.find("a")
            if not a_link:
                continue

            key_gold = li.find("span", class_="KeyGold")
            if not key_gold and "article" in a_link["href"]:
                return "https://asahi.com" + a_link["href"]

    raise ValueError(f"Could not find any article on page {url}")


if __name__ == "__main__":
    import random

    section = random.choice(sections)
    print(get_links(section))
