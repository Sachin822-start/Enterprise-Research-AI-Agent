from models.state import ResearchState

from services.scraper_service import scrape_page
from services.chroma_service import (
    document_exists,
    store_document
)


def scraper_node(state: ResearchState):
    print("\n" + "=" * 60)
    print("SCRAPER AGENT")
    print("=" * 60)
    documents = []

    for article in state["search_results"]:
        url = article["url"]
        if document_exists(url):
            print(f"Already Exists : {url}")
            continue
        print(f"Scraping : {url}")
        text = scrape_page(url)
        if len(text) < 500:
            continue

        document = {
            "title": article["title"],
            "url": url,
            "topic": state["topic"],
            "text": text
        }
        store_document(document)
        documents.append(document)
    state["documents"] = documents
    print("\nDocuments Added :", len(documents))
    return state