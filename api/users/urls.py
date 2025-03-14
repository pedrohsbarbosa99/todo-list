from .views import get_users, create_user

urlpatterns = [
    ("GET", "/users", get_users),
    ("POST", "/users", create_user),
]
