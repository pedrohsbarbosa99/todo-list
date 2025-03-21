import uuid

from core.database.config import connection
from core.service.auth.utils import make_password


class User:

    @staticmethod
    def list():
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM account")
            users = cursor.fetchall()

        return users

    @staticmethod
    def retrieve(id):
        with connection.cursor() as cursor:

            cursor.execute("SELECT username FROM account WHERE id = $1", (id,))
            user = cursor.fetchone()

        return user

    @staticmethod
    def retrieve_by_username_for_auth(username):
        with connection.cursor() as cursor:

            cursor.execute(
                "SELECT id, username, password FROM account WHERE username = $1",
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
                "INSERT INTO account (id, username, password) VALUES ($1, $2, $3)",
                (str(uuid.uuid4()), data["username"], make_password(password)),
            )

    @staticmethod
    def delete(id):
        with connection.cursor() as cursor:

            cursor.execute("DELETE FROM account WHERE id = $1", (id,))

    @staticmethod
    def update(self, id, data):
        with connection.cursor() as cursor:

            cursor.execute(
                """
                UPDATE user
                SET username = COALESCE($1, username)
                WHERE id = $2
                """,
                (data.get("username"), id),
            )
