from api.response import success_response
from core.service.auth.authentication import JWTAuthentication
from core.service.auth.decorators import authentication_class
from core.service.user import UserService

user = UserService()


@authentication_class(auth_class=JWTAuthentication)
def get_users(request):
    return success_response(user.list())


def create_user(request):
    data = request.body

    user.create(data)

    return success_response(status=201)


@authentication_class(auth_class=JWTAuthentication)
def retrieve_user(request, pk):
    return success_response(user.retrieve(pk))


@authentication_class(auth_class=JWTAuthentication)
def delete_user(request, pk):
    user.delete(pk)

    return success_response(status=204)


@authentication_class(auth_class=JWTAuthentication)
def update_user(request, pk):
    data = request.body

    user.update(pk, data)

    return success_response(status=204)
