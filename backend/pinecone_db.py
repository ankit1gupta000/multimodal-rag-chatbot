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

def store_vector(id, embedding, text):

    index.upsert(
        vectors=[
            {
                "id": id,
                "values": embedding,
                "metadata": {
                    "text": text
                }
            }
        ]
    )

def search_vector(embedding):

    result = index.query(
        vector=embedding,
        top_k=3,
        include_metadata=True
    )

    return result