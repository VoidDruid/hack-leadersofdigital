from typing import List, Union

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from conf import service_settings
from crud import create_program as create_program_
from crud import get_program as get_program_
from crud import get_programs as get_programs_
from database import Program, ProgramCreateSchema, ProgramSchema
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
    offset: int = 0,
    limit: int = service_settings.MAX_LIMIT,
    category: str = None,
) -> Union[Response, List[Program]]:
    return paginate(get_programs_(db, category), Program, offset, limit)


@api.post('/program', response_model=ProgramSchema, responses=extra)
def create_event(
    program: ProgramCreateSchema, db: Session = Depends(get_db)
) -> Union[Response, Program]:
    return create_program_(db=db, program=program)
