import uuid

from core.database.config import get_db


class Task:

    @staticmethod
    def list(user_id):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                "SELECT id, title, description, completed FROM tasks WHERE user_id = ?",
                (user_id,),
            )
            tasks = cursor.fetchall()

        return tasks

    @staticmethod
    def retrieve(id):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                "SELECT title, description, completed FROM tasks WHERE id = ?", (id,)
            )
            task = cursor.fetchone()

        return task

    @staticmethod
    def create(data, user_id):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO tasks (id, user_id, title, description) VALUES (?, ?, ?, ?)",
                (
                    str(uuid.uuid4()),
                    user_id,
                    data["title"],
                    data["description"],
                ),
            )

            db.commit()

    @staticmethod
    def delete(id):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))

            db.commit()

    def update(id, data):
        with get_db() as db:
            cursor = db.cursor()

            cursor.execute(
                """
                UPDATE tasks 
                SET title = COALESCE(?, title),
                description = COALESCE(?, description)
                WHERE id = ?
                """,
                (data.get("title"), data.get("description"), id),
            )

            db.commit()
