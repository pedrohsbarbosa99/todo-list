from core.service.auth.authentication import JWTAuthentication
from api.response import success_response, error_response


def login(request):
    username = request.body.get("username")
    password = request.body.get("password")

    token = JWTAuthentication().get_token(request, username, password)

    if not token:
        return error_response(message="Invalid username or password", status=401)

    return success_response(data={"token": token})


def logout(request):
    return success_response(message="Logout successful")


def refresh_token(request):
    return success_response(message="Refresh token successful")
