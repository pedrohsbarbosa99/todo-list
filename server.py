from wsgi import application

if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    httpd = make_server("127.0.0.1", 8000, application)
    print(f"Servidor WSGI rodando em http://127.0.0.1:8000")
    httpd.serve_forever()
