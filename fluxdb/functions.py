from .create_app import create_app
from .migrate import migrate
from .makemigration import create_migration

functions_map = {
    "create_app": {
        "function": create_app,
        "args": [],
    },
    "migrate": {"function": migrate, "args": []},
    "create_migration": {
        "function": create_migration,
        "args": [
            {
                "required": True,
                "name": "name",
                "flag": "-n",
                "help": "Migration Name",
                "type": str,
            },
            {
                "required": True,
                "name": "dir",
                "flag": "-d",
                "help": "Directory where migration is located",
                "type": str,
            },
        ],
    },
}
