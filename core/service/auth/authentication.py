from datetime import datetime
from core.service.auth.jwt import JWT
from core.service.user import UserService
from core.service.auth.utils import is_valid_password


class JWTAuthentication:
    def get_token(self, request, username, password):
        user = UserService().retrieve_by_username_for_auth(username)

        if not user:
            return

        if not is_valid_password(user["password"], password):
            return

        request.user_id = user["id"]

        return JWT().encode(user)

    def authenticate(self, request):
        token = request.headers.get("Authorization")

        if not token:
            return False

        jwt = JWT()

        is_token_valid = jwt.is_valid(token)

        if not is_token_valid:
            return False

        _, payload = jwt.decode(token)

        if datetime.now() > datetime.fromtimestamp(payload["exp"]):
            return False

        user = UserService().retrieve_by_username_for_auth(payload["username"])

        if not user:
            return False

        request.user_id = user["id"]

        return True
