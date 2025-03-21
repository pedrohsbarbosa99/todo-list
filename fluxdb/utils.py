import dxpq
from .config import DATABASE_URL


def check_table_migration_exists():
    connection = dxpq.Connection(DATABASE_URL)
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT EXISTS (
                SELECT 1 FROM pg_tables 
                WHERE tablename = 'fluxdb_migration'
            );
            """
        )
        result = cursor.fetchone()
        return result.get("exists", False) is True
