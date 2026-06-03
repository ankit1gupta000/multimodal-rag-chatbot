from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)


def ask_groq(
    context,
    question
):

    prompt = f"""
You are a document question answering assistant.

Rules:

1. Answer ONLY from the context.
2. Do NOT use external knowledge.
3. If answer is not present in context, reply:

"This information is not present in the uploaded document."

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": (
                    "Please provide a concise direct answer to the Question. "
                    "Do NOT include or repeat the Context, and do NOT quote chunks.\n\n"
                    + prompt
                )
            }
        ],
        temperature=0
    )

    return (
        response
        .choices[0]
        .message.content
    )