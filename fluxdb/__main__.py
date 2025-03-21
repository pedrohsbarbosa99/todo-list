import argparse
from .functions import functions_map


def parse_arguments():
    parser = argparse.ArgumentParser(description="CLI for fluxdb")
    parser.add_argument(
        "--command",
        "-c",
        type=str,
        help="Command to execute",
        required=True,
    )
    args, _ = parser.parse_known_args()
    function_map = functions_map.get(args.command)

    subparser = argparse.ArgumentParser(parents=[parser], conflict_handler="resolve")

    for kwargs in function_map["args"]:
        name = kwargs.pop("name")
        subparser.add_argument(
            f"--{name}",
            f"{kwargs.pop("flag")}",
            **kwargs,
        )
        kwargs["name"] = name

    return subparser.parse_args()


def build_kwargs(function_map, args):
    kwargs = {}
    for kwarg in function_map["args"]:
        name = kwarg["name"]
        kwargs[name] = getattr(args, name)
    return kwargs


def main():
    args = parse_arguments()

    command = args.command

    function_map = functions_map.get(command)

    if command:
        func = function_map["function"]

        func(**build_kwargs(function_map, args))
    else:
        print(f"Unknown command {command}")


if __name__ == "__main__":
    main()
