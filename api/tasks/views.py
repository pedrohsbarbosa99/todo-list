from core.service.task import TaskService
from core.service.auth.decorators import authentication_class
from core.service.auth.authentication import JWTAuthentication
from api.response import success_response

task = TaskService()


@authentication_class(auth_class=JWTAuthentication)
def list_tasks(request):
    return success_response(task.list(request.user_id))


@authentication_class(auth_class=JWTAuthentication)
def retrieve_task(request, pk):
    return success_response(task.retrieve(pk))


@authentication_class(auth_class=JWTAuthentication)
def create_task(request):
    task.create(request.body, request.user_id)
    return success_response(status=204)


@authentication_class(auth_class=JWTAuthentication)
def delete_task(pk):
    task.delete(pk)
    return success_response(status=204)


@authentication_class(auth_class=JWTAuthentication)
def update_task(request, pk):
    task.update(pk, request.body)
    return success_response(status=204)
