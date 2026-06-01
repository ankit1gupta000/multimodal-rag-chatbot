import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

vision_model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def generate_embedding(text):
    result = genai.embed_content(
        model="models/embedding-001",
        content=text
    )

    return result["embedding"]