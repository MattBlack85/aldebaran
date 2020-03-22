import os

from databases import Database

DB_PORT = os.environ.get('DB_PORT', '9432')
DB_NAME = os.environ.get('DB_NAME', 'covid_test')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'password')
DB_USER = os.environ.get('DB_USER', 'aldebaran')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
TESTING = os.environ.get('TESTING', True)
DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

database = Database(DB_URL)


async def init_db():
    await database.connect()


async def close_db():
    await database.disconnect()
