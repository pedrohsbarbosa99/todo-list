FROM python:3.13-slim

WORKDIR /app

COPY . /app

EXPOSE 8000

ENV HOST=""
ENV PORT=80

RUN apt-get update && \
    apt-get install -y gcc build-essential libpq-dev python3-dev git

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["python", "server.py"]