import datetime
from typing import List, Union, Optional

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from conf import service_settings
from crud import create_program as create_program_
from crud import get_program as get_program_
from crud import get_programs as get_programs_
from database.models import Program, ProgramCreateSchema, ProgramSchema
from services.api import extra
from services.dependencies import get_db
from services.utils import paginate

from . import api


@api.get('/program/{id}', response_model=ProgramSchema)
def get_program(program_id: int, db: Session = Depends(get_db)) -> Program:
    return get_program_(db, program_id)


@api.get('/program', response_model=List[ProgramSchema], responses=extra)
def programs_list(
    db: Session = Depends(get_db),
    offset: Optional[int] = 0,
    limit: Optional[int] = service_settings.MAX_LIMIT,
    category: Optional[str] = None,
    start_time: Optional[datetime.datetime] = None,
    end_time: Optional[datetime.datetime] = None,
) -> Union[Response, List[Program]]:
    query = get_programs_(db, category)
    if start_time:
        query = query.filter(Program.created_at >= start_time)
    if end_time:
        query = query.filter(Program.created_at <= end_time)
    return paginate(query, Program, offset, limit)


@api.post('/program', response_model=ProgramSchema, responses=extra)
def create_event(
    program: ProgramCreateSchema, db: Session = Depends(get_db)
) -> Union[Response, Program]:
    return create_program_(db=db, program=program)
