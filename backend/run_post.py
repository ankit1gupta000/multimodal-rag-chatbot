import requests
p=r"c:\Users\ankit\OneDrive\Desktop\multimodel chatbot\test_upload.pdf"
with open(p,'rb') as f:
    r=requests.post('http://127.0.0.1:8001/upload-document', data=f.read(), headers={'Content-Type':'application/pdf'}, timeout=30)
    print('Status:', r.status_code)
    print(r.text)
