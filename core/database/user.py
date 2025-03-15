import uuid

from core.database.config import get_db
from core.service.auth.utils import make_password


class User:

    @staticmethod
    def list():
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()

        return users

    @staticmethod
    def retrieve(id):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("SELECT username FROM users WHERE id = ?", (id,))
            user = cursor.fetchone()

        return user

    @staticmethod
    def retrieve_by_username_for_auth(username):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                "SELECT id, username, password FROM users WHERE username = ?",
                (username,),
            )
            user = cursor.fetchone()
            if not user:
                return

        return (
            {
                "id": user["id"],
                "username": user["username"],
                "password": user["password"],
            }
            if user
            else {}
        )

    @staticmethod
    def create(data):
        password = data.get("password")
        username = data.get("username")

        if not password or not username:
            return

        with get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO users (id, username, password) VALUES (?, ?, ?)",
                (str(uuid.uuid4()), data["username"], make_password(password)),
            )

            db.commit()

    @staticmethod
    def delete(id):
        with get_db() as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (id,))

            db.commit()

    @staticmethod
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
