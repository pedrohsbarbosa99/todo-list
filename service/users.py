import uuid
from core.database import get_db


class User:
    def list(self):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()

        return [{"id": user["id"], "username": user["username"]} for user in users]

    def retrieve(self, id):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT username FROM users WHERE id = ?", (id,))
            user = cursor.fetchone()

        return {"username": user["username"]} if user else {}

    def retrieve_by_username_for_auth(self, username):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                "SELECT id, username, password FROM users WHERE username = ?",
                (username,),
            )
            user = cursor.fetchone()
            if not user:
                return

        return {"id": user["id"], "username": user["username"]} if user else {}

    def create(self, data):
        password = data.get("password")
        username = data.get("username")

        if not password or not username:
            return

        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO users (id, username, password) VALUES (?, ?, ?)",
                (str(uuid.uuid4()), data["username"], password),
            )

            db.commit()

    def delete(self, id):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (id,))

            db.commit()

    def update(self, id, data):
        with get_db() as db:
            cursor = db.cursor()

            cursor.execute(
                """
                UPDATE users 
                SET username = COALESCE(?, username)
                WHERE id = ?
                """,
                (data.get("username"), id),
            )

            db.commit()
