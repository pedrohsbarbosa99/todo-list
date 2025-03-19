import json
from functools import cached_property

from core.database.config import init_db
from core.urls import routes
from dongle.utils import find_matching_route


class WSGIApp:
    def __init__(self):
        init_db()

    def __call__(self, environ, start_response):
        request = WSGIRequest(environ)

        handler, params = find_matching_route(routes, request.method, request.path)

        if handler:
            if params:
                response, status = handler(request, **params)
            else:
                response, status = handler(request)

            status_text = f"{status} {'OK' if 200 <= status <= 399 else 'ERROR'}"
        else:
            response = {"error": "Rota não encontrada"}
            status = 404
            status_text = "404 Not Found"

        response_body = json.dumps(response).encode()

        headers = [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(response_body))),
        ]

        start_response(status_text, headers)

        return [response_body]


class WSGIRequest:
    def __init__(self, environ):
        self.environ = environ
        self.headers = self._parse_headers()

    @property
    def method(self):
        return self.environ["REQUEST_METHOD"]

    @property
    def path(self):
        return self.environ["PATH_INFO"]

    @cached_property
    def body(self):
        content_length = int(self.environ.get("CONTENT_LENGTH", 0) or 0)

        if content_length > 0:
            request_body = self.environ["wsgi.input"].read(content_length)
            try:
                return json.loads(request_body.decode())
            except json.JSONDecodeError:
                return {}
        return {}

    @cached_property
    def query_params(self):
        return self.environ.get("QUERY_STRING", "")

    def _parse_headers(self):
        headers = {}
        for key, value in self.environ.items():
            if key.startswith("HTTP_"):
                header_name = key[5:].replace("_", "-").title()
                headers[header_name] = value
            elif key in ("CONTENT_TYPE", "CONTENT_LENGTH"):
                header_name = key.replace("_", "-").title()
                headers[header_name] = value

        class HeadersAdapter:
            def __init__(self, headers_dict):
                self.headers_dict = headers_dict

            def get(self, name, default=None):
                return self.headers_dict.get(name, default)

        return HeadersAdapter(headers)

    def send_response(self, code):
        pass

    def send_header(self, keyword, value):
        pass

    def end_headers(self):
        pass

    def log_message(self, format, *args):
        pass


application = WSGIApp()
