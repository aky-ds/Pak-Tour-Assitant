import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def tavily_search(query: str):

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=5,
    )

    results = []

    for item in response.get("results", []):
        title = item.get("title", "")
        content = item.get("content", "")

        results.append(
            f"{title}\n{content}"
        )

    return "\n\n".join(results)