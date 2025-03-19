FROM python:3.13-slim

WORKDIR /app

COPY . /app

EXPOSE 8000

ENV HOST=""
ENV PORT=80

RUN apt-get update && \
    apt-get install -y git

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "wsgi:application"]
