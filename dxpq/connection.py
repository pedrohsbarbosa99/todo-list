import dxpq_ext  # type: ignore


class Connection:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def cursor(self):
        return Cursor.from_connection(dxpq_ext.PGConnection(self.connection_string))


class Cursor:
    def __init__(self, connection, cursor):
        self.connection = connection
        self._cursor = cursor

    @classmethod
    def from_connection(cls, connection):
        return cls(connection, dxpq_ext.PGCursor(connection))

    def execute(self, sql: str, params=None):
        if params is not None:
            return self._cursor.execute_params(sql, params)
        return self._cursor.execute(sql)

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    def close(self):
        self._cursor.close()
        self.connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __del__(self):
        self.close()
