from functools import partial
from typing import Any

from cachetools import cached, TTLCache
from cachetools.keys import hashkey
from sqlalchemy.orm import Session

from conf import service_settings
from database.models import Config
from database.utils import upsert

TYPE_NAMES = {
    int: 'integer',
    str: 'string',
    bool: 'boolean',
    list: 'array',
}

TYPE_NAMES_REVERSE = {value: key for key, value in TYPE_NAMES.items()}
TYPE_NAMES_REVERSE['array'] = lambda val: val.split(',')

PROGRAM_THRESHOLD_KEY = 'program_threshold'
PROGRAM_MAX_HOURS_KEY = 'program_max_hours'

DEFAULT_CONFIGS = {
    PROGRAM_THRESHOLD_KEY: 80,
    PROGRAM_MAX_HOURS_KEY: 500,
}


def cache_key(*args, **kwargs):
    return hashkey(*args[1:], **kwargs)  # pop db: Session


config_cache = TTLCache(1000, service_settings.CONFIG_CACHE_TTL)
cache = cached(config_cache, cache_key)


@cache
def get_config_value(db: Session, key: str) -> Any:
    config = db.query(Config).filter(Config.name == key).one_or_none()
    if config is None:
        if key in DEFAULT_CONFIGS:
            value = DEFAULT_CONFIGS[key]
            config = Config(key=key, type=TYPE_NAMES[type(value)], value=value)
            db.add(config)
            db.commit()
        else:
            return None
    return TYPE_NAMES_REVERSE[config.type](config.value)


def set_config_value(db: Session, key: str, value: Any) -> None:  # TODO: return updated config
    upsert(db, Config, key=key, value=value, type=TYPE_NAMES[type(value)])


get_program_threshold = partial(get_config_value, key=PROGRAM_THRESHOLD_KEY)
get_program_max_hours = partial(get_config_value, key=PROGRAM_MAX_HOURS_KEY)
