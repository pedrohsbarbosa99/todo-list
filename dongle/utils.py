import re
import sys
from importlib import import_module
from urllib.parse import urlparse


def cached_import(module_path, class_name):
    # Check whether module is loaded and fully initialized.
    if not (
        (module := sys.modules.get(module_path))
        and (spec := getattr(module, "__spec__", None))
        and getattr(spec, "_initializing", False) is False
    ):
        module = import_module(module_path)
    return getattr(module, class_name)


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    try:
        return cached_import(module_path, class_name)
    except AttributeError as err:
        raise ImportError(
            'Module "%s" does not define a "%s" attribute/class'
            % (module_path, class_name)
        ) from err


def find_matching_route(routes, method, path):
    parsed_url = urlparse(path)
    path_without_query = parsed_url.path

    for (route_method, route_pattern), handler in routes.items():
        if method != route_method:
            continue

        if "<" not in route_pattern:
            if path_without_query == route_pattern:
                return handler, {}
            continue

        regex_pattern = route_pattern
        param_specs = re.findall(r"<([^:]+):([^>]+)>", route_pattern)

        for param_type, param_name in param_specs:
            if param_type == "uuid":
                regex = r"(?P<{0}>[0-9a-f]{{8}}-[0-9a-f]{{4}}-[0-9a-f]{{4}}-[0-9a-f]{{4}}-[0-9a-f]{{12}})".format(
                    param_name
                )
            elif param_type == "int":
                regex = r"(?P<{0}>\d+)".format(param_name)
            elif param_type == "str":
                regex = r"(?P<{0}>[^/]+)".format(param_name)
            else:
                regex = r"(?P<{0}>[^/]+)".format(param_name)

            regex_pattern = regex_pattern.replace(f"<{param_type}:{param_name}>", regex)

        regex_pattern = f"^{regex_pattern}$"
        regex_obj = re.compile(regex_pattern)

        match = regex_obj.match(path_without_query)
        if match:
            params = match.groupdict()
            return handler, params

    return None, {}
