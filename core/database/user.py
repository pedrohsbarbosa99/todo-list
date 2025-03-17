import uuid

from core.database.config import connection
from core.service.auth.utils import make_password


class User:

    @staticmethod
    def list():
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()

        return users

    @staticmethod
    def retrieve(id):
        with connection.cursor() as cursor:

            cursor.execute("SELECT username FROM users WHERE id = ?", (id,))
            user = cursor.fetchone()

        return user

    @staticmethod
    def retrieve_by_username_for_auth(username):
        with connection.cursor() as cursor:

            cursor.execute(
                "SELECT id, username, password FROM users WHERE username = $1",
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

        with connection.cursor() as cursor:

            cursor.execute(
                "INSERT INTO users (id, username, password) VALUES (?, ?, ?)",
                (str(uuid.uuid4()), data["username"], make_password(password)),
            )

    @staticmethod
    def delete(id):
        with connection.cursor() as cursor:

            cursor.execute("DELETE FROM users WHERE id = ?", (id,))

    @staticmethod
    def update(self, id, data):
        with connection.cursor() as cursor:

            cursor.execute(
                """
                UPDATE users 
                SET username = COALESCE(?, username)
                WHERE id = ?
                """,
                (data.get("username"), id),
            )
