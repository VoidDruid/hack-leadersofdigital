import functools
from typing import List, Type, TypeVar, Union

from sqlalchemy.orm import Query
from starlette.responses import Response

from conf import service_settings

from .api import Error, NotFoundError

T = TypeVar('T')


def paginate(query: Query, model: Type[T], offset: int, limit: int) -> Union[Response, List[T]]:
    if limit > service_settings.MAX_LIMIT:
        raise Error(f'Maximum limit is {service_settings.MAX_LIMIT}!')
    return query.order_by(model.id).offset(offset).limit(limit).all()


def raise_on_none(func):

    @functools.wraps(func)
    def decorated(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            raise NotFoundError('Not found')
        return result

    return decorated
