from mongoengine import connect
from ..config.env import DATABASE_URL, DATABASE_USER, DATABASE_NAME, DATABASE_PASSWORD


def setup_database():
    connect(host=f"mongodb://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_URL}/{DATABASE_NAME}?authSource=admin")



