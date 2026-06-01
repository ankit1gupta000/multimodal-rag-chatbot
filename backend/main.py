from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from gemini_service import vision_model
from embedding_service import get_embedding
from pinecone_db import store_vector, search_vector

import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Multimodal RAG Backend Running"
    }


@app.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    question: str = Form(...)
):
    try:
        image = Image.open(file.file)

        # Generate image description
        response = vision_model.generate_content(
            [
                "Describe this image in detail",
                image
            ]
        )

        description = response.text

        # Create embedding
        embedding = get_embedding(description)

        # Store in Pinecone
        store_vector(
            str(uuid.uuid4()),
            embedding,
            description
        )
        print("Stored Description:")
        print(description)

        # Answer question about image
        answer = vision_model.generate_content(
            [
                question,
                image
            ]
        )

        return {
            "description": description,
            "answer": answer.text
        }

    except Exception as e:
        return {
            "error": str(e)
        }


@app.post("/ask")
async def ask(
    question: str = Form(...)
):
    try:
        # Convert question to embedding
        question_embedding = get_embedding(question)

        # Search Pinecone
        results = search_vector(question_embedding)
        print(results)
        print("PINECONE RESULTS:")
        print(results)

        context = ""

        # Pinecone v9 format
        if hasattr(results, "matches"):

            for match in results.matches:

                if hasattr(match, "metadata"):
                    context += (
                        match.metadata.get("text", "")
                        + "\n"
                    )

        # Fallback for older SDKs
        elif isinstance(results, dict):

            for match in results.get("matches", []):

                context += (
                    match.get("metadata", {})
                    .get("text", "")
                    + "\n"
                )

        if context.strip() == "":
            return {
                "answer": "No relevant images found in memory."
            }

        prompt = f"""
You are a helpful AI assistant.

Context:
{context}

Question:
{question}

Answer using the context above.
"""

        response = vision_model.generate_content(
            prompt
        )

        return {
            "context": context,
            "answer": response.text
        }

    except Exception as e:
        return {
            "error": str(e)
        }