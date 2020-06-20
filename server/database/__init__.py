# pylint: disable=C0413

from typing import Any

from pymongo import MongoClient

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from conf import PG_URI, MONGO_URI, mongo_settings

SQLALCHEMY_DATABASE_URL = PG_URI
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base: Any = declarative_base()

from .models import *  # isort:skip


class Mongo:
    def __getattr__(self, item):
        return getattr(self.mongo_db, item)

    def __init__(self):
        self.mongo_client = MongoClient(MONGO_URI)
        self.mongo_db = self.mongo_client[mongo_settings.DATABASE_NAME]


__all__ = [
    'Base',
    'Session',
    'Mongo',
]
