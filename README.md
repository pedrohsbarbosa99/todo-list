# Meu Projeto TodoList

Este projeto é uma implementação de um servidor HTTP simples em Python.

Criei os módulos `dongle` e `dxpq`.

## Dongle

A `dongle` é uma biblioteca Python que implementa um sistema de manipulação de **URLs**, **configuração de rotas** e **handlers** associados a essas rotas. Ela é útil em sistemas onde você precisa configurar e lidar com rotas e suas respectivas ações, de forma mais simplificada e customizável, de maneira similar ao sistema de rotas do Django, mas sem a necessidade de bibliotecas externas.

A biblioteca fornece uma forma prática e eficiente de configurar e gerenciar URLs e suas ações em um servidor HTTP, ideal para quem quer construir rotas personalizadas de maneira flexível.

## DXPQ

A `dxpq` é uma biblioteca Python que inclui uma extensão escrita em C para fornecer uma interface mais rápida e direta de comunicação com um banco de dados PostgreSQL. A biblioteca foi construída para ser usada diretamente em Python, permitindo a comunicação eficiente com o PostgreSQL sem depender de bibliotecas externas como `psycopg2`. 

Ao usar a extensão em C, a biblioteca `dxpq` proporciona um acesso mais direto e de alto desempenho ao banco de dados.

## Objetivo

O objetivo deste projeto é criar um **todo-list** em Python, sem o uso de bibliotecas externas (exceto aquelas listadas em `requirements-dev.txt`). O foco é usar apenas módulos personalizados e garantir que todas as funcionalidades sejam implementadas manualmente.

## Estrutura do Projeto

```bash
.
├── api
│   ├── auth
│   │   ├── urls.py
│   │   └── views.py
│   ├── response.py
│   ├── tasks
│   │   ├── urls.py
│   │   └── views.py
│   └── users
│   │   ├── urls.py
│   │   └── views.py
├── core
│   ├── config.py
│   ├── database
│   │   ├── config.py
│   │   ├── task.py
│   │   └── user.py
│   ├── models.py
│   ├── service
│   │   ├── auth
│   │   │   ├── authentication.py
│   │   │   ├── decorators.py
│   │   │   ├── jwt.py
│   │   │   └── utils.py
│   │   ├── task
│   │   │   └── service.py
│   │   └── user
│   │       └── service.py
│   └── urls.py
├── database.db
├── dockerfile
├── dongle
│   ├── handlers.py
│   ├── urls
│   │   └── conf.py
│   └── utils.py
├── LICENSE
├── README.md
└── server.py
```


## Como executar o Projeto

Clone o repositório:
```bash
git clone git@github.com:pedrohsbarbosa99/todo-list.git
```

Entre na pasta do projeto:
```bash
cd todo-list
```

Instale as dependências do PostgreSQL:
```bash
sudo apt-get install libpq-dev python3-dev
```

Instale as dependências de Dev:
```bash
pip install -r requirements-dev.txt
```

Buildar a biblioteca `dxpq`:
```bash
cd dxpq && ./build.sh && cd ..
```

Execute o servidor:
```bash
python server.py
```

## Rotas

