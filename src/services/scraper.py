import requests
from bs4 import BeautifulSoup
import services.logger as logger
from typing import List, Dict
from urllib.parse import urlparse
import time


def extract_text_from_websites(urls: List[str]) -> List[Dict[str, str]]:
    results = []

    for url in urls:
        try:
            if not urlparse(url).scheme:
                url = "https://" + url

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            for script in soup(["script", "style"]):
                script.decompose()

            text = soup.get_text(separator=" ", strip=True)

            results.append({"url": url, "raw_text": text})

            logger.debug(f"Finished scraping {url}")
            time.sleep(0.1)

        except Exception as e:
            logger.debug(f"Failed to scrape {url}: {str(e)}")
            continue

    return results
