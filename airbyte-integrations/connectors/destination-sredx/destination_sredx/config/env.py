import os

# DataBase
DATABASE_URL = os.environ.get("DATABASE_URL", "localhost:27018")
DATABASE_USER = os.environ.get("DATABASE_USER", "root")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "password")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "sredx")
