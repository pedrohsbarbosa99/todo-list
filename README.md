# Meu Projeto Web com Dongle

Este projeto é uma implementação de um servidor HTTP simples em Python, que usa o módulo `dongle` para registrar rotas de forma semelhante ao sistema de URLs do Django.

## Objetivo

Meu objetivo é criar um todo-list em python, sem uso de nenhuma biblioteca externa.

## Estrutura do Projeto

``` bash
├── api
│   ├── __init__.py
│   └── users
│       ├── urls.py
│       └── views.py
├── core
│   ├── config.py
│   ├── database.py
│   ├── __init__.py
│   ├── models.py
│   └── urls.py
├── dongle
│   ├── handlers.py
│   ├── __init__.py
│   ├── urls
│   │   ├── conf.py
│   │   └── __init__.py
│   └── utils.py
├── README.md
└── server.py
```

# Como executar o Projeto

Clone o repositorio:
```bash
git clone git@github.com:pedrohsbarbosa99/todo-list.git
```

Execute o servidor:
```bash
python server.py
```

## Rotas

- `GET /users`: Retorna uma lista de todos os usuarios.
- `POST /users`: Cria um novo usuario.
