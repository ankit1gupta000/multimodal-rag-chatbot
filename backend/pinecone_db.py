from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()

pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

index = pc.Index(
    os.getenv("PINECONE_INDEX")
)


def store_vector(
    vector_id,
    embedding,
    text,
    doc_type="document"
):

    index.upsert(
        vectors=[
            {
                "id": str(vector_id),
                "values": embedding,
                "metadata": {
                    "text": text,
                    "type": doc_type
                }
            }
        ]
    )


def search_vector(
    embedding,
    top_k=5
):

    return index.query(
        vector=embedding,
        top_k=top_k,
        include_metadata=True
    )