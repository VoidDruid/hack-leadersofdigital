from typing import List, Union

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from conf import service_settings
from crud import get_discipline as get_discipline_
from crud import get_disciplines as get_disciplines_
from database import Discipline, DisciplineSchema
from services.api import Error, extra
from services.dependencies import get_db
from services.utils import paginate

from . import api


@api.get('/discipline/{id}', response_model=DisciplineSchema)
def get_discipline(id: int, db: Session = Depends(get_db)) -> Discipline:
    return get_discipline_(db, id)


@api.get('/parameter', response_model=List[DisciplineSchema], responses=extra)
def parameters_list(
    db: Session = Depends(get_db),
    category: str = None,
    offset: int = 0,
    limit: int = service_settings.MAX_LIMIT,
) -> Union[Response, List[Discipline]]:
    return paginate(get_disciplines_(db, category), Discipline, offset, limit)
