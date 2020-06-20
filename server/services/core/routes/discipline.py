from typing import List, Union

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from conf import service_settings
from crud import create_discipline as create_discipline_
from crud import get_discipline as get_discipline_
from crud import get_disciplines as get_disciplines
from database.models import (
    Discipline,
    DisciplineCreateSchema,
    DisciplineFullSchema,
    DisciplineSchema,
)
from services.api import extra
from services.dependencies import get_pg
from services.utils import paginate, raise_on_none

from . import api


@api.get('/discipline/{id}', response_model=DisciplineSchema)
@raise_on_none
def get_discipline(id: int, db: Session = Depends(get_pg)) -> Discipline:
    return get_discipline_(db, id)


@api.get('/discipline', response_model=List[DisciplineSchema], responses=extra)
def get_disciplines_list(
    db: Session = Depends(get_pg),
    category: str = None,
    offset: int = 0,
    limit: int = service_settings.MAX_LIMIT,
) -> List[Discipline]:
    return paginate(get_disciplines(db, category), Discipline, offset, limit)


@api.post('/discipline', response_model=DisciplineFullSchema)
def create_discipline(
    discipline: DisciplineCreateSchema, db: Session = Depends(get_pg),
) -> Discipline:
    return create_discipline_(db, discipline)
