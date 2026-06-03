import json
import tempfile
from http.server import HTTPServer, BaseHTTPRequestHandler
from pdf_service import extract_pdf_text, chunk_text

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/upload-document":
            self.send_response(404)
            self.end_headers()
            return

        content_type = self.headers.get('content-type', '')
        # Support raw PDF POSTs with content-type 'application/pdf'
        if content_type.startswith('application/pdf'):
            length = int(self.headers.get('content-length', 0))
            data = self.rfile.read(length)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                tmp.write(data)
                tmp_path = tmp.name

            text = extract_pdf_text(tmp_path)
            chunks = chunk_text(text)
            count = len(chunks)
            summary = text[:400]

            resp = {"summary": summary, "chunks_stored": count}
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode())
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error":"unsupported content type"}')

if __name__ == '__main__':
    server_address = ('', 8001)
    httpd = HTTPServer(server_address, Handler)
    print('Test server running on port 8001')
    httpd.serve_forever()
