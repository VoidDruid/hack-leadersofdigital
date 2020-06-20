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
from crud import update_program as update_program_
from database.models import Program, ProgramCreateSchema, ProgramSchema
from services.api import extra
from services.dependencies import get_pg
from services.utils import paginate, raise_on_none
from worker.tasks import process_program

from . import api


def queue_program(program: Program) -> None:
    process_program.delay(program.id)


class ProgramSpider(BaseModel):
    id: int
    name: str
    rating: Optional[int] = 128
    is_deleted: bool
    disciplines: List[Dict[str, str]]
    category: str


class MiniDiscipline(BaseModel):
    id: int
    name: str


class YearDiff(BaseModel):
    added: List[MiniDiscipline]
    removed: List[MiniDiscipline]


class YearStats(BaseModel):
    diff: YearDiff
    rating: int = 0


@api.get('/program/stats', response_model=Dict[int, YearStats], responses=extra)
def programs_stats_list(db: Session = Depends(get_pg)) -> Union[Response, Dict]:
    programs: List[Program] = get_programs_(db, None).order_by(Program.created_at).all()
    stats_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for p in programs:
        stats_dict[p.created_at.year]['diff']['added'].append({'id': p.id, 'name': p.name})
        if p.deleted_at is not None:
            stats_dict[p.created_at.year]['diff']['removed'].append({'id': p.id, 'name': p.name})
    return stats_dict


@api.get('/program/spider', response_model=List[ProgramSpider], responses=extra)
def programs_spider_list(
    db: Session = Depends(get_pg),
    category: Optional[str] = None
) -> Union[Response, List]:
    programs: List[Program] = get_programs_(db, category).order_by(Program.created_at).all()
    spider_list = []
    for p in programs:
        entity = {
            'id': p.id,
            'is_deleted': True if p.deleted_at is not None else False,
            'name': p.name,
            'disciplines': [],
            'category': p.category,
        }
        for disc in p.disciplines:
            entity['disciplines'].append({'name': disc.name, 'category': disc.category})
        spider_list.append(entity)
    return spider_list


@api.get('/program/{id}', response_model=ProgramSchema, responses=extra('not_found'))
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
    program = create_program_(db=db, program=program)
    queue_program(program)
    return program


@api.patch('/program/{id}', response_model=ProgramSchema, responses=extra('not_found'))
def update_program(
    program_id: int, program_base: ProgramCreateSchema, db: Session = Depends(get_pg)
) -> Union[Response, Program]:
    program = update_program_(db, program_id, program_base)
    queue_program(program)
    return program
