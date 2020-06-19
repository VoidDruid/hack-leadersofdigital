from typing import List, Union, TypeVar, Type

from sqlalchemy.orm import Query
from starlette.responses import Response

from conf import service_settings

from .api import Error

T = TypeVar('T')


def paginate(
    query: Query, model: Type[T], offset: int, limit: int
) -> Union[Response, List[T]]:
    if limit > service_settings.MAX_LIMIT:
        return Error(f'Maximum limit is {service_settings.MAX_LIMIT}!')
    return query.order_by(model.id).offset(offset).limit(limit).all()
