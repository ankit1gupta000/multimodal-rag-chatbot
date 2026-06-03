from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from vision_service import describe_image
from pdf_service import (
    extract_pdf_text,
    chunk_text
)

from embedding_service import get_embedding
from pinecone_db import store_vector, search_vector
from groq_service import ask_groq

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


# ==========================
# IMAGE UPLOAD
# ==========================

@app.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    question: str = Form(...)
):
    try:

        image = Image.open(file.file)

        description = describe_image(
            image
        )

        embedding = get_embedding(
            description
        )

        store_vector(
            str(uuid.uuid4()),
            embedding,
            description,
            "image"
        )

        answer = (
            f"Image description: "
            f"{description}"
        )

        return {
            "description": description,
            "answer": answer
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# ==========================
# PDF UPLOAD
# ==========================

@app.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...)
):
    try:

        text = extract_pdf_text(
            file.file
        )

        chunks = chunk_text(text)

        count = 0

        for chunk in chunks:

            embedding = get_embedding(
                chunk
            )

            store_vector(
                str(uuid.uuid4()),
                embedding,
                chunk,
                "document"
            )

            count += 1

        # Generate summary (use model, but fall back to local extract on failure)
        try:
            summary = ask_groq(
                text[:4000],
                "Give a concise summary of this document."
            )
        except Exception as e:
            print("SUMMARY ERROR:", str(e))
            # Fallback: use the first 400 characters of extracted text
            summary = text[:400] if text else "No text could be extracted from the document."

        return {
            "summary": summary,
            "chunks_stored": count
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# ==========================
# MEMORY Q&A
# ==========================

@app.post("/ask")
async def ask(
    question: str = Form(...)
):
    try:

        question_embedding = get_embedding(
            question
        )

        results = search_vector(
            question_embedding
        )

        context_chunks = []

        if hasattr(
            results,
            "matches"
        ):

            for match in results.matches:

                if (
                    hasattr(
                        match,
                        "metadata"
                    )
                    and match.metadata
                ):

                    if (
                        match.metadata.get(
                            "type"
                        )
                        == "document"
                    ):

                        context_chunks.append(
                            match.metadata.get(
                                "text",
                                ""
                            )
                        )

        context = "\n".join(
            context_chunks
        )

        if not context.strip():

            return {
                "answer":
                "No relevant information found in uploaded documents."
            }

        answer = ask_groq(
            context,
            question
        )

        return {
            "answer": answer
        }

    except Exception as e:

        print(
            "ASK ERROR:",
            str(e)
        )

        return {
            "error": str(e)
        }