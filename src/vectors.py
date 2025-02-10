import chromadb

chroma_client = chromadb.Client()


def create_service_collection(service: str):
    collection = chroma_client.get_or_create_collection(service)
    return collection


def add_documents(service: str, documents: list[str]):
    collection = chroma_client.get_collection(service)
    collection.add(documents)


def query(service: str, query: str, n_results: int = 10):
    collection = chroma_client.get_collection(service)
    results = collection.query(query_texts=[query], n_results=n_results)
    return results
