import scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class Scraper(scrapy.Spider):
    name = "scraper"

    def __init__(self, websites: list[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.websites = websites

    def start(self):
        for website in self.websites:
            yield scrapy.Request(url=website, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        raw_text = soup.get_text(separator=" ", strip=True)

        yield {
            "url": response.url,
            "raw_text": raw_text,
        }


def extract_text_from_websites(websites: list[str]) -> list[dict]:
    results = []

    def on_item_scraped(item):
        results.append(item)

    process = CrawlerProcess(get_project_settings())
    crawler = process.create_crawler(Scraper)
    crawler.signals.connect(on_item_scraped, signal=scrapy.signals.item_scraped)

    process.crawl(crawler, websites=websites)
    process.start()
    return results
