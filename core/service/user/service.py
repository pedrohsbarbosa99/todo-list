from core.database.user import User


class UserService:
    def __init__(self):
        self.repository = User

    def list(self):
        users = self.repository.list()
        return [{"id": user["id"], "username": user["username"]} for user in users]

    def retrieve(self, id):
        user = self.repository.retrieve(id)
        return {"id": user["id"], "username": user["username"]} if user else {}

    def retrieve_by_username_for_auth(self, username):
        return self.repository.retrieve_by_username_for_auth(username)

    def create(self, data):
        return self.repository.create(data)

    def delete(self, id):
        return self.repository.delete(id)

    def update(self, id, data):
        return self.repository.update(id, data)
