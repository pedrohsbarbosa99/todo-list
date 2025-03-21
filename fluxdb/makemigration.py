import os, re, math, datetime
from pathlib import Path


def _make_nex_migration_value(last_migration_value):
    value = 3 / last_migration_value
    if value < 1:
        value = 0
    zeros = math.ceil(value)
    return f'{"0" * zeros}{last_migration_value + 1}'


def create_migration(dir, name):
    template_file = (
        open(os.path.join(os.path.dirname(__file__), "templates", "migration.py"))
        .read()
        .replace("<datetime_now>", str(datetime.datetime.now()))
    )

    path = Path(dir)

    files = filter(lambda x: re.findall(r"\d+\_.+\.py", str(x)), path.glob("*py"))

    data = sorted([re.sub(r"[^?!\d+]", "", str(file)) for file in files])

    last_migration_value = int(data[-1]) if data else 0

    value = _make_nex_migration_value(last_migration_value)

    migration_name = f"{value}_{name.lower().replace(" ", "_")}.py"

    with path.joinpath(migration_name).open(mode="w") as file:
        file.write(template_file)

    print(f"file {path.joinpath(migration_name)} created")
