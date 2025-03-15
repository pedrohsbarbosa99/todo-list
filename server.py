import os
from http.server import HTTPServer

from core.database.config import init_db
from dongle.handlers import RequestHandler

HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", 8000))


def run_server():
    init_db()
    server = HTTPServer((HOST, PORT), RequestHandler)
    print(f"Servidor rodando em http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
