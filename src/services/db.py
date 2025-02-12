import chromadb
import services.logger as logger
from uuid import uuid4

chroma_client = chromadb.PersistentClient(path="./chroma_db")


def create_service_collection(service: str):
    normalized_service_name = normalize_service_name(service)
    collection = chroma_client.get_or_create_collection(normalized_service_name)
    logger.debug(
        f"Created collection for {service} with name {normalized_service_name}"
    )
    return collection


def add_documents(service: str, documents: list[str]):
    normalized_service_name = normalize_service_name(service)
    collection = chroma_client.get_collection(normalized_service_name)
    ids = [str(uuid4()) for _ in documents]
    collection.add(documents=documents, ids=ids)


def query(service: str, query: str, n_results: int = 5):
    normalized_service_name = normalize_service_name(service)
    collection = chroma_client.get_collection(normalized_service_name)
    results = collection.query(query_texts=[query], n_results=n_results)
    return results


def normalize_service_name(service: str) -> str:
    normalized = "".join(c if c.isalnum() else "_" for c in service.lower())

    while "__" in normalized:
        normalized = normalized.replace("__", "_")

    normalized = normalized.strip("_")

    if len(normalized) < 3:
        normalized = normalized + "_" * (3 - len(normalized))

    normalized = normalized[:63]

    return normalized
