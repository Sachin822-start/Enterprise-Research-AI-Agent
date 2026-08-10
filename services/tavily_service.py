import os

from tavily import TavilyClient
from dotenv import load_dotenv
from config import TAVILY_API_KEY
load_dotenv()

# client = TavilyClient(
#     api_key=os.getenv("TAVILY_API_KEY")
# )
client = TavilyClient(api_key=TAVILY_API_KEY)

def search_web(query):

    response = client.search(
    query=query,
    search_depth="advanced",
    max_results=4,
    include_answer=False,
    include_raw_content=False
)
    results = []

    for item in response["results"]:

        results.append(
            {
                "title": item["title"],
                "url": item["url"],
                "content": item.get("content", "")
            }
        )

    return results