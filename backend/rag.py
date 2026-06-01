from gemini_service import generate_embedding
from pinecone_db import search_vector

def retrieve_context(question):
    embedding = generate_embedding(question)

    results = search_vector(embedding)

    contexts = []

    for match in results["matches"]:
        contexts.append(
            match["metadata"]["text"]
        )

    return "\n".join(contexts)