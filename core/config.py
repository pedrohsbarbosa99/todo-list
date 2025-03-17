import os

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "n7*h*eqb*41yrqi9hwif#m#0d)!)p%%we^v%*-v54inkh7wc^&",
)


DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/todolist",
)
