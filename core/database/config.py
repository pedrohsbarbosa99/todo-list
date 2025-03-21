import dxpq
from core.config import DATABASE_URL

connection = dxpq.Connection(DATABASE_URL)
