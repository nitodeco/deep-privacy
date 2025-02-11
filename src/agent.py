from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor, as_completed
from config.prompts import (
    service_description_prompt,
    search_queries_prompt,
    answer_question_prompt,
    summarize_prompt,
)
from config.questions import questions

from services.ai import generate_completion, generate_structured_completion
from services.scraper import extract_text_from_websites
from services.search import search
from services.db import create_service_collection, add_documents, query
from services.utils import join_strings, save_to_file
import services.logger as logger
import time


class SearchQueries(BaseModel):
    queries: list[str]


def generate_privacy_report(service: str) -> str:
    total_start_time = time.time()
    logger.info(f"Generating privacy report for {service}")
    start_time = time.time()
    research(service)
    logger.info(f"Finished researching {service} in {time.time() - start_time} seconds")
    start_time = time.time()
    answers = process_questions(service)
    logger.info(
        f"Finished processing questions for {service} in {time.time() - start_time} seconds"
    )
    start_time = time.time()
    summary = summarize(
        f"The service is called {service}. Information: {join_strings(answers)}"
    )
    logger.info(f"Finished summarizing {service} in {time.time() - start_time} seconds")
    logger.info(
        f"Finished generating privacy report for {service} in {time.time() - total_start_time} seconds"
    )
    save_report(service, summary)
    return summary


def save_report(service: str, summary: str):
    save_to_file(f"{service}.md", summary, "reports")


def summarize(text: str) -> str:
    response = generate_completion(summarize_prompt, text)
    return response


def process_questions(service: str) -> list[str]:
    answers = []
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(answer_question, service, question)
            for question in questions
        ]
        answers = [future.result() for future in as_completed(futures)]
    return answers


def research(service: str) -> list[str]:
    service_description = generate_service_description(service)
    search_queries = generate_search_queries(service, service_description)

    create_service_collection(service)

    with ThreadPoolExecutor() as executor:
        search_futures = [
            executor.submit(search, query) for query in search_queries.queries
        ]
        search_results = [future.result() for future in as_completed(search_futures)]

        urls = [page["href"] for results in search_results for page in results]

        scrape_futures = [
            executor.submit(extract_text_from_websites, [url]) for url in urls
        ]
        scraped_results = [future.result() for future in as_completed(scrape_futures)]

        for results in scraped_results:
            if results:
                texts = [
                    result["raw_text"] for result in results if result.get("raw_text")
                ]
                if texts:
                    add_documents(service, texts)


def answer_question(service: str, question: str) -> str:
    query_results = query(service, question, 10)
    response = generate_completion(
        answer_question_prompt,
        f"Question: {question}\n\nQuery Results: {query_results}",
    )
    return response


def generate_service_description(service: str) -> str:
    user_message = f"Generate a description for {service}"
    response = generate_completion(service_description_prompt, user_message)
    return response


def generate_search_queries(service: str, description: str) -> SearchQueries:
    user_message = (
        f"Generate 10 search queries for {service}. Description: {description}"
    )
    response = generate_structured_completion(
        search_queries_prompt, user_message, response_format=SearchQueries
    )
    return response
