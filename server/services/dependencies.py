from typing import Generator

from database import Mongo, Session


def get_pg() -> Generator[Session, None, None]:
    db = None
    try:
        db = Session()
        yield db
    finally:
        if db:
            db.close()


def get_mongo():
    mongo = None
    try:
        mongo = Mongo()
        yield mongo
    finally:
        if mongo:
            mongo.mongo_client.close()
