from ai import generate_response
from scaper import extract_text_from_websites
from search import search
from vectors import create_service_collection, add_documents, query
from pydantic import BaseModel
from config.prompts import service_description_prompt, search_queries_prompt


class SearchQueries(BaseModel):
    queries: list[str]


def research(service: str) -> list[str]:
    service_description = generate_service_description(service)
    search_queries = generate_search_queries(service, service_description)

    create_service_collection(service)

    for query in search_queries.queries:
        result = search(query)
        for page in result:
            text = extract_text_from_websites([page.href])
            add_documents(service, [text])


def generate_service_description(service: str) -> str:
    user_message = f"Generate a description for {service}"
    response = generate_response(service_description_prompt, user_message)
    return response.choices[0].message.content


def generate_search_queries(service: str, description: str) -> SearchQueries:
    user_message = (
        f"Generate 10 search queries for {service}. Description: {description}"
    )
    response = generate_response(
        search_queries_prompt, user_message, response_format=SearchQueries
    )
    return response.choices[0].message.parsed
