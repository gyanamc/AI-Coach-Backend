import os
from langchain_community.tools import DuckDuckGoSearchResults
from serpapi import GoogleSearch

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def google_search(query: str):
    try:
        params = {"q": query, "api_key": GOOGLE_API_KEY, "num": 5}
        search = GoogleSearch(params)
        results = search.get_dict()
        snippets = "\n".join(
            [r.get("snippet", "") for r in results.get("organic_results", [])]
        )
        return snippets or "No results found via Google."
    except Exception as e:
        print("⚠️ Google Search failed:", e)
        return None

def duckduckgo_search(query: str):
    try:
        search = DuckDuckGoSearchResults()
        return search.run(query)
    except Exception as e:
        print("⚠️ DuckDuckGo Search failed:", e)
        return "Search unavailable."

def get_search_results(query: str, engine: str = "google"):
    """Tries Google SERP first, falls back to DuckDuckGo."""
    if engine == "google" and GOOGLE_API_KEY:
        result = google_search(query)
        if result:
            return result
    print("🔁 Falling back to DuckDuckGo...")
    return duckduckgo_search(query)
