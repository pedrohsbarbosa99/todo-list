import json
from functools import cached_property
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse

from core.urls import routes
from dongle.utils import find_matching_route


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.handle_request("GET")

    def do_POST(self):
        self.handle_request("POST")

    def do_PUT(self):
        self.handle_request("PUT")

    def do_DELETE(self):
        self.handle_request("DELETE")

    def do_PATCH(self):
        self.handle_request("PATCH")

    def handle_request(self, method):
        handler, params = find_matching_route(routes, method, self.path)

        if handler:
            if params:
                response, status = handler(self, **params)
            else:
                response, status = handler(self)
            self.send_response(status)
        else:
            response = {"error": "Rota não encontrada"}
            self.send_response(404)

        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    @cached_property
    def body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        data = json.loads(body.decode())
        return data

    @cached_property
    def query_params(self):
        parsed_url = urlparse(self.path)
        return parsed_url.query
