import json

users_db = []


def get_users(_):
    return {"users": users_db}, 200


def create_user(request):
    data = request.body

    if "name" not in data:
        return {"error": "O campo name é obrigatorio"}, 400

    user = {"id": len(users_db) + 1, "name": data["name"]}
    users_db.append(user)

    return {"message": f"Usuário {data['name']} criado!", "user": user}, 400
