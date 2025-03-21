import dxpq
from core.config import DATABASE_URL
from uuid import uuid4

connection = dxpq.Connection(DATABASE_URL)


def upgrade():
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO account (id, username, password) VALUES
            ('{id1}', 'user1', 'hashed_password_1'),
            ('{id2}', 'user2', 'hashed_password_2'),
            ('{id3}', 'user3', 'hashed_password_3')
            RETURNING id;
            """.format(
                id1=uuid4(), id2=uuid4(), id3=uuid4()
            )
        )
        cursor.execute(
            """
            INSERT INTO task (id, user_id, title, description, completed) VALUES
            ('{tid1}', (SELECT id FROM account WHERE username='user1'), 'Task 1', 'Description 1', FALSE),
            ('{tid2}', (SELECT id FROM account WHERE username='user1'), 'Task 2', 'Description 2', TRUE),
            ('{tid3}', (SELECT id FROM account WHERE username='user2'), 'Task 3', 'Description 3', FALSE),
            ('{tid4}', (SELECT id FROM account WHERE username='user3'), 'Task 4', 'Description 4', TRUE);
            """.format(
                tid1=uuid4(), tid2=uuid4(), tid3=uuid4(), tid4=uuid4()
            )
        )
        print("DADOS INSERIDOS")


def downgrade():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM task;")
        cursor.execute("DELETE FROM account;")
        print("DADOS REMOVIDOS")
