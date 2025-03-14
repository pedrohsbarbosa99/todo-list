from http.server import BaseHTTPRequestHandler
import json
from core.urls import routes


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.handle_request("GET")

    def do_POST(self):
        self.handle_request("POST")

    def do_PUT(self):
        self.handle_request("PUT")

    def do_DELETE(self):
        self.handle_request("DELETE")

    def handle_request(self, method):
        handler = routes.get((method, self.path))
        if handler:
            response, status = handler(self)
            self.send_response(status)
        else:
            response = {"error": "Rota não encontrada"}
            self.send_response(404)

        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    @property
    def body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        data = json.loads(body.decode())
        return data
