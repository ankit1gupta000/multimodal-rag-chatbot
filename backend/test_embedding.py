from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

response = client.models.embed_content(
    model="text-embedding-004",
    contents="A dog playing in a park"
)

print(response)