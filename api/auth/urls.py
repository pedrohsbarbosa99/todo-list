from .views import login, logout, refresh_token

urlpatterns = [
    ("POST", "/login", login),
    ("POST", "/logout", logout),
    ("POST", "/refresh-token", refresh_token),
]
