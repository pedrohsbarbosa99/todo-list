from importlib import import_module


def include(arg):
    urlconf_module = arg

    if isinstance(urlconf_module, str):
        urlconf_module = import_module(urlconf_module)

    patterns = getattr(urlconf_module, "urlpatterns", urlconf_module)

    return {(method, path): view for method, path, view in patterns}


def build_routers(urlpatterns):
    return {k: v for data in urlpatterns for k, v in data.items()}
