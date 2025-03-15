from functools import wraps


def authentication_class(auth_class):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = args[0]
            auth_instance = auth_class()

            if not auth_instance.authenticate(request):
                return {"error": "Unauthorized"}, 401

            return func(*args, **kwargs)

        return wrapper

    return decorator
