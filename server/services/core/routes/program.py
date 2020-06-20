import datetime
from collections import defaultdict
from typing import Any, Dict, List, Optional, Union

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.responses import Response

from conf import service_settings
from crud import create_program as create_program_
from crud import get_program as get_program_
from crud import get_programs as get_programs_
from database.models import Program, ProgramCreateSchema, ProgramSchema
from services.api import extra
from services.dependencies import get_pg
from services.utils import paginate, raise_on_none

from . import api


class ProgramStats(BaseModel):
    diff: Optional[Dict[str, List[Dict[str, str]]]]
    rating: Optional[int] = 0


class ProgramSpider(BaseModel):
    id: int
    name: str
    rating: Optional[int] = 128
    is_deleted: bool
    disciplines: List[Dict[str, str]]


@api.get('/program/stats', response_model=Dict[int, ProgramStats], responses=extra)
def programs_stats_list(db: Session = Depends(get_pg)) -> Union[Response, Dict]:
    programs: List[Program] = get_programs_(db, None).order_by(Program.created_at).all()
    stats_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for p in programs:
        stats_dict[p.created_at.year]['diff']['added'].append({'id': p.id, 'name': p.name})
        if p.deleted_at is not None:
            stats_dict[p.created_at.year]['diff']['removed'].append({'id': p.id, 'name': p.name})
    return stats_dict


@api.get('/program/spider', response_model=List[ProgramSpider], responses=extra)
def programs_stats_list(db: Session = Depends(get_pg)) -> Union[Response, List]:
    programs: List[Program] = get_programs_(db, None).order_by(Program.created_at).all()
    spider_list: List[ProgramSpider] = list()
    for p in programs:
        entity = {
            'id': p.id,
            'is_deleted': True if p.deleted_at is not None else False,
            'name': p.name,
            'disciplines': [],
        }
        for disc in p.disciplines:
            entity['disciplines'].append({'name': disc.name, 'category': disc.category})
        spider_list.append(entity)
    return spider_list


@api.get('/program/{id}', response_model=ProgramSchema)
@raise_on_none
def get_program(program_id: int, db: Session = Depends(get_pg)) -> Program:
    return get_program_(db, program_id)


@api.get('/program', response_model=List[ProgramSchema], responses=extra)
def programs_list(
    db: Session = Depends(get_pg),
    offset: Optional[int] = 0,
    limit: Optional[int] = service_settings.MAX_LIMIT,
    category: Optional[str] = None,
    start_time: Optional[datetime.datetime] = None,
    end_time: Optional[datetime.datetime] = None,
) -> List[Program]:
    query = get_programs_(db, category)
    if start_time:
        query = query.filter(Program.created_at >= start_time)
    if end_time:
        query = query.filter(Program.created_at <= end_time)
    return paginate(query, Program, offset, limit)


@api.post('/program', response_model=ProgramSchema, responses=extra)
def create_event(program: ProgramCreateSchema, db: Session = Depends(get_pg)) -> Program:
    return create_program_(db=db, program=program)
