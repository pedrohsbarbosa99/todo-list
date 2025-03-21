import uuid

from core.database.config import connection


class Task:

    @staticmethod
    def list(user_id):
        with connection.cursor() as cursor:
            tasks = cursor.fetchall(
                "SELECT id, title, description, completed FROM task WHERE user_id = $1",
                (user_id,),
            )

        return tasks

    @staticmethod
    def retrieve(id):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT title, description, completed FROM task WHERE id = $1", (id,)
            )
            task = cursor.fetchone()

        return task

    @staticmethod
    def create(data, user_id):
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO task (id, user_id, title, description) VALUES ($1, $2, $3, $4) RETURNING id",
                (
                    str(uuid.uuid4()),
                    user_id,
                    data["title"],
                    data["description"],
                ),
            )

            task_id = cursor.fetchone()

        return task_id

    @staticmethod
    def delete(id):
        with connection.cursor() as cursor:

            cursor.execute("DELETE FROM task WHERE id = $1", (id,))

    def update(id, data):
        with connection.cursor() as cursor:

            cursor.execute(
                """
                UPDATE task
                SET title = COALESCE($1, title),
                description = COALESCE($2, description)
                WHERE id = $3
                """,
                (data.get("title"), data.get("description"), id),
            )
