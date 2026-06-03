from embedding_service import get_embedding
from pinecone_db import search_vector

def retrieve_context(question):

    embedding = get_embedding(question)

    results = search_vector(embedding)

    contexts = []

    for match in results["matches"]:

        if "metadata" in match and "text" in match["metadata"]:
            contexts.append(match["metadata"]["text"])

    return "\n".join(contexts)