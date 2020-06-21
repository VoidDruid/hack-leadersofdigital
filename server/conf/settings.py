# pylint: disable=W0401,C0413,W0614

import os
from typing import Optional

from pydantic import BaseSettings


class Level:
    LOCAL = 'local'
    DEV = 'dev'
    PROD = 'prod'


RUN_LEVEL = os.getenv('RUN_LEVEL', Level.LOCAL)

DEBUG = False
from conf.envs.prod import *  # isort: ignore

if RUN_LEVEL in (Level.DEV, Level.LOCAL):
    from conf.envs.dev import *  # isort: ignore
if RUN_LEVEL == Level.LOCAL:
    from conf.envs.local import *  # isort: ignore


class AppSettings(BaseSettings):
    class Config:
        env_prefix = 'APP_'


class PostgresSettings(AppSettings):
    PG_NAME: str = PG_NAME
    PG_USER: str = PG_USER
    PG_PASSWORD: str = PG_PASSWORD
    PG_HOST: str = PG_HOST
    PG_PORT: str = PG_PORT


class MongoSettings(AppSettings):
    MONGO_NAME: str = MONGO_NAME
    MONGO_USER: str = MONGO_USER
    MONGO_PASSWORD: str = MONGO_PASSWORD
    MONGO_HOST: str = MONGO_HOST
    MONGO_PORT: str = MONGO_PORT


class RedisSettings(AppSettings):
    REDIS_HOST: str = REDIS_HOST
    REDIS_PORT: str = REDIS_PORT
    CELERY_TASKS_DB: str = CELERY_TASKS_DB
    CELERY_RESULT_DB: str = CELERY_RESULTS_DB


class ServiceSettings(AppSettings):
    MAX_LIMIT: int = 20
    CONFIG_CACHE_TTL: int = 60
    SCAN_PROGRAMS_DELAY: int = 120


service_settings = ServiceSettings()
pg_settings = PostgresSettings()
redis_settings = RedisSettings()
mongo_settings = MongoSettings()


def make_pg_uri(
    user: str = pg_settings.PG_USER,
    password: str = pg_settings.PG_PASSWORD,
    host: str = pg_settings.PG_HOST,
    port: str = pg_settings.PG_PORT,
    db: Optional[str] = pg_settings.PG_NAME,
) -> str:
    connection_string = f'postgresql+psycopg2://{user}:{password}@{host}:{port}'
    if db:
        connection_string += f'/{db}'
    return connection_string


def make_mongo_uri(
    user: str = mongo_settings.MONGO_USER,
    password: str = mongo_settings.MONGO_PASSWORD,
    host: str = mongo_settings.MONGO_HOST,
    port: str = mongo_settings.MONGO_PORT,
) -> str:
    connection_string = f'mongodb://{user}:{password}@{host}:{port}'
    return connection_string


PG_URI = make_pg_uri()
MONGO_URI = make_mongo_uri()
