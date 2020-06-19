from functools import partial
from typing import Any

from sqlalchemy.orm import Session

from database.models import Config

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


def set_config_value(db: Session, key: str, value: Any) -> Config:


get_program_threshold = partial(get_config_value, key=PROGRAM_THRESHOLD_KEY)
get_program_max_hours = partial(get_config_value, key=PROGRAM_MAX_HOURS_KEY)
