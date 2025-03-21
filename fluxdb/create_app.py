import os
from pathlib import Path

import dxpq
from .exceptions import MigrationAppAlreadyExists
from .config import DATABASE_URL
from .utils import check_table_migration_exists


def create_app():
    connection = dxpq.Connection(DATABASE_URL)
    with connection.cursor() as cursor:
        table_exists = check_table_migration_exists()
        if table_exists:
            raise MigrationAppAlreadyExists("Migration app already exists on database")

        fd = open(os.path.join(os.path.dirname(__file__), "database/create.sql"))
        cursor.execute(fd.read())
        fd.close()
