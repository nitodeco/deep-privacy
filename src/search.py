from duckduckgo_search import DDGS


def search(query: str, max_results: int = 10):
    return DDGS().text(query, max_results=max_results, region="us-en")
