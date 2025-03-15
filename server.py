import os
from http.server import HTTPServer
from dongle.handlers import RequestHandler
from core.database import init_db

HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", 8000))

init_db()


def run_server():
    server = HTTPServer((HOST, PORT), RequestHandler)
    print(f"Servidor rodando em http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
