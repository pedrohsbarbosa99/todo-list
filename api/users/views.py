from service.users import User

users_db = []

user = User()


def get_users(request):
    return user.list(), 200


def create_user(request):
    data = request.body

    user.create(data)

    return {"message": f"Usuário {data['username']} criado!"}, 200


def retrieve_user(request, pk):
    return user.retrieve(pk), 200


def delete_user(request, pk):
    user.delete(pk)

    return {"message": f"Usuário {pk} deletado!"}, 200


def update_user(request, pk):
    data = request.body

    user.update(pk, data)

    return {"message": f"Usuário {pk} atualizado!"}, 200
