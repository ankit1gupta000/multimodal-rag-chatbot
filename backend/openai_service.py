from openai import OpenAI
import os
from dotenv import load_dotenv
import base64
from PIL import Image
import io

# Lazily create the OpenAI client so importing this module doesn't fail
# when the environment variable isn't set. A runtime error will be raised
# only when an OpenAI call is attempted without a configured key.
_client = None

# Load .env from the backend folder so running via uvicorn/pip picks up keys
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Please set it in the environment or backend/.env"
            )
        try:
            _client = OpenAI(api_key=api_key)
        except TypeError as e:
            # Some httpx/openai package version mismatches cause a
            # `Client.__init__() got an unexpected keyword argument 'proxies'` error
            # when proxy-related env vars are present. Retry after clearing them.
            msg = str(e)
            if "proxies" in msg:
                proxy_keys = [
                    "HTTP_PROXY",
                    "HTTPS_PROXY",
                    "http_proxy",
                    "https_proxy",
                    "NO_PROXY",
                    "no_proxy",
                ]
                saved = {k: os.environ.pop(k) for k in proxy_keys if k in os.environ}
                try:
                    _client = OpenAI(api_key=api_key)
                except Exception:
                    # restore env and re-raise original error with guidance
                    os.environ.update(saved)
                    raise RuntimeError(
                        "Failed to initialize OpenAI client due to an incompatibility with proxy settings. "
                        "Try upgrading the 'openai' and 'httpx' packages (pip install -U openai httpx), "
                        "or ensure no conflicting proxy environment variables are set."
                    )
            else:
                raise
    return _client


def get_embedding(text):
    """Get embeddings using OpenAI's text-embedding-3-small model"""
    client = _get_client()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def ask_openai(context, question):
    """Ask OpenAI a question based on provided context"""
    client = _get_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You answer ONLY from the uploaded document context.
If the answer is not found in the document, reply: I cannot find that information in the uploaded document."""
            },
            {
                "role": "user",
                "content": f"""Context:
{context}

Question:
{question}"""
            }
        ]
    )
    return response.choices[0].message.content


def describe_image(image: Image.Image):
    """Describe an image using OpenAI's vision capabilities"""
    # Convert PIL Image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    base64_image = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
    
    client = _get_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "Describe this image in detail."
                    }
                ]
            }
        ]
    )
    return response.choices[0].message.content


def summarize_text(text):
    """Summarize text using OpenAI"""
    client = _get_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Please provide a concise summary of this text:\n\n{text}"
            }
        ]
    )
    return response.choices[0].message.content
