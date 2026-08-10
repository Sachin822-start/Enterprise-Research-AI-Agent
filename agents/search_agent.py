from models.state import ResearchState
from services.tavily_service import search_web


def search_node(state: ResearchState):
    print("\n" + "=" * 60)
    print("SEARCH AGENT")
    print("=" * 60)
    search_results = []
    unique_urls = set()
    total_sources = 0

    for query in state["search_queries"]:
        print(f"\nSearching : {query}")
        results = search_web(query)
        for article in results:
            url = article["url"]
            if url in unique_urls:
                continue
            unique_urls.add(url)
            search_results.append(article)
            total_sources += 1
    state["search_results"] = search_results
    print("\n" + "=" * 60)
    print(f"Unique Sources Collected : {total_sources}")
    print("=" * 60)
    return state