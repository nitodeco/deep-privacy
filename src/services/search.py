from duckduckgo_search import DDGS
import services.logger as logger


def search(query: str, max_results: int = 10):
    logger.info(f"Searching duckduckgo for {query}")
    results = DDGS().text(query, max_results=max_results, region="us-en")
    logger.info(f"Found {len(results)} results")
    return results
