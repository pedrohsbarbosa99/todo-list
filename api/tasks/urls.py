from .views import create_task, delete_task, list_tasks, retrieve_task, update_task

urlpatterns = [
    ("GET", "/tasks", list_tasks),
    ("POST", "/tasks", create_task),
    ("GET", "/tasks/<uuid:pk>", retrieve_task),
    ("DELETE", "/tasks/<uuid:pk>", delete_task),
    ("PATCH", "/tasks/<uuid:pk>", update_task),
]
