from core.database.task import Task


class TaskService:
    def __init__(self):
        self.repository = Task

    def list(self, user_id):
        tasks = self.repository.list(user_id)
        return [{"id": task["id"], "title": task["title"]} for task in tasks]

    def retrieve(self, id):
        task = self.repository.retrieve(id)
        return {"id": task["id"], "title": task["title"]} if task else {}

    def create(self, data, user_id):
        return self.repository.create(data, user_id)

    def delete(self, id):
        return self.repository.delete(id)

    def update(self, id, data):
        return self.repository.update(id, data)
