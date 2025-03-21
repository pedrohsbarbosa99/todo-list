import os, glob
import logging

import dxpq
from .config import MIGRATION_DIRS, DATABASE_URL
from .exceptions import MigrationAppDontExists, MigrationFailedException
from importlib.util import spec_from_file_location, module_from_spec
from .utils import check_table_migration_exists

logger = logging.getLogger(__name__)

IGNORED_FILES = ["__init__.py"]

connection = dxpq.Connection(DATABASE_URL)


class Migration:
    def __is_valid_file(self, file):
        return file.split("/")[-1] not in IGNORED_FILES

    def _get_unnaplied_migration_from_dir(self, migration_dir):
        migration_files = self._get_migration_files(migration_dir)

        files_filtered_to_migrate = filter(
            self.__is_valid_file,
            migration_files,
        )

        files = ",".join(files_filtered_to_migrate)

        with connection.cursor(cursor_type="dict") as cursor:
            cursor.execute(
                """
                WITH files_received AS (
                    SELECT UNNEST(string_to_array($1, ',')) AS file
                )
                SELECT *
                FROM files_received 
                WHERE file NOT IN (
                    SELECT file FROM fluxdb_migration WHERE applied IS TRUE
                )
                ORDER BY files_received.file;
                """,
                (files,),
            )
            return cursor.fetchall()

    def _registry_migrate(self, file, applied):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO fluxdb_migration (file, applied)
                VALUES ($1, $2)
                ON CONFLICT (file) DO UPDATE
                SET applied = $2;
                """,
                (file, applied),
            )

    def _get_module(self, module_name, file):
        spec = spec_from_file_location(module_name, file)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def __apply_func(self, func):
        err = ""
        applied = False

        try:
            func()
            applied = True
        except Exception as e:
            err = str(e)

        return applied, err

    def _apply(self, file_to_migrate, module_name):
        upgrade_err = ""
        downgrade_err = ""
        applied = False

        file = file_to_migrate["file"]

        module = self._get_module(module_name, file)

        upgrade_func, downgrade_func = self._get_migration_functions(module)

        if upgrade_func:
            logger.info(f"applying migration {file}...")
            applied, upgrade_err = self.__apply_func(upgrade_func)

            self._registry_migrate(file, applied=applied)
            logger.info(f"migration {file} applied")

        return applied, upgrade_err or downgrade_err

    def _get_migration_functions(self, module):
        upgrade_func = getattr(module, "upgrade", None)
        downgrade_func = getattr(module, "downgrade", None)
        return upgrade_func, downgrade_func

    def _get_module_name(self, migration_dir):
        return migration_dir.replace("/", ".")

    def _get_migration_files(self, migration_dir):
        return glob.glob(os.path.join(migration_dir, "*.py"))


def migrate():
    applied_migrations = False
    migration = Migration()
    table_exists = check_table_migration_exists()
    if not table_exists:
        raise MigrationAppDontExists("Migration App don't exists")

    for migration_dir in MIGRATION_DIRS:
        module_name = migration._get_module_name(migration_dir)

        files_to_migrate = migration._get_unnaplied_migration_from_dir(migration_dir)

        for file_to_migrate in files_to_migrate:
            applied, err = migration._apply(file_to_migrate, module_name)

            if not applied:
                raise MigrationFailedException(err)

            applied_migrations = True

    if not applied_migrations:
        print("No Migration to apply")
