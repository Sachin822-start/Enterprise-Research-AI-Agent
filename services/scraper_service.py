import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def scrape_page(url):
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )
        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for tag in soup(
            [
                "script",
                "style",
                "noscript",
                "header",
                "footer",
                "nav"
            ]
        ):
            tag.decompose()
        text = soup.get_text(
            separator=" ",
            strip=True
        )
        return text
    except Exception:
        return ""