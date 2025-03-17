import uuid

from core.database.config import connection


class Task:

    @staticmethod
    def list(user_id):
        with connection.cursor() as cursor:
            tasks = cursor.fetchall(
                "SELECT id, title, description, completed FROM tasks WHERE user_id = ?",
                (user_id,),
            )

        return tasks

    @staticmethod
    def retrieve(id):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT title, description, completed FROM tasks WHERE id = ?", (id,)
            )
            task = cursor.fetchone()

        return task

    @staticmethod
    def create(data, user_id):
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO tasks (id, user_id, title, description) VALUES (?, ?, ?, ?) RETURNING id",
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

            cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))

    def update(id, data):
        with connection.cursor() as cursor:

            cursor.execute(
                """
                UPDATE tasks 
                SET title = COALESCE(?, title),
                description = COALESCE(?, description)
                WHERE id = ?
                """,
                (data.get("title"), data.get("description"), id),
            )
