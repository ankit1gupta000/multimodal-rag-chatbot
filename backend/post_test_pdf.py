import requests
import os

url = "http://127.0.0.1:8000/upload-document"
file_path = os.path.join(os.path.dirname(__file__), "..", "test_upload.pdf")

with open(file_path, "rb") as f:
    files = {"file": ("test_upload.pdf", f, "application/pdf")}
    try:
        r = requests.post(url, files=files, timeout=30)
        print("Status:", r.status_code)
        try:
            print(r.json())
        except Exception:
            print(r.text)
    except Exception as e:
        print("Request error:", e)
