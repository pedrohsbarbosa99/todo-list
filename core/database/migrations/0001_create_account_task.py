import dxpq
from core.config import DATABASE_URL

connection = dxpq.Connection(DATABASE_URL)


def upgrade():
    with connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS account (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS task (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                user_id UUID NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (user_id) REFERENCES account(id) ON DELETE CASCADE
            );
            """
        )
        print("TABELAS CRIADAAS")


def downgrade():
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DROP TABLE IF EXISTS account;
            DROP TABLE IF EXISTS task;
            """
        )
