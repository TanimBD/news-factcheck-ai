import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_news(query):

    response = tavily.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    results = []

    for r in response["results"]:

        text = f"""
Title: {r.get('title')}
URL: {r.get('url')}
Content: {r.get('content')}
"""

        results.append(text)

    return "\n".join(results)