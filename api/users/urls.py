from .views import create_user, delete_user, get_users, retrieve_user, update_user

urlpatterns = [
    ("GET", "/users", get_users),
    ("POST", "/users", create_user),
    ("GET", "/users/<uuid:pk>", retrieve_user),
    ("DELETE", "/users/<uuid:pk>", delete_user),
    ("PATCH", "/users/<uuid:pk>", update_user),
]
