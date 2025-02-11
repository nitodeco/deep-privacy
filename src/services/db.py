import chromadb
import services.logger as logger
from uuid import uuid4

chroma_client = chromadb.PersistentClient(path="./chroma_db")


def create_service_collection(service: str):
    collection = chroma_client.get_or_create_collection(service)
    logger.debug(f"Created collection for {service}")
    return collection


def add_documents(service: str, documents: list[str]):
    collection = chroma_client.get_collection(service)
    ids = [str(uuid4()) for _ in documents]
    collection.add(documents=documents, ids=ids)
    logger.debug(f"Added {len(documents)} documents to {service}")


def query(service: str, query: str, n_results: int = 10):
    collection = chroma_client.get_collection(service)
    results = collection.query(query_texts=[query], n_results=n_results)
    logger.debug(f"Queried {service} and got {len(results)} results")
    return results
