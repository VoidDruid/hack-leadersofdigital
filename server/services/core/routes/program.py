from typing import List, Union

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from conf import service_settings
from crud import get_program as get_program_
from crud import get_programs as get_programs_
from crud import create_program as create_program_
from database import Program, ProgramSchema, ProgramCreateSchema
from services.api import Error, extra
from services.dependencies import get_db

from . import api


@api.get('/program/{id}', response_model=ProgramSchema)
def get_program(program_id: int, db: Session = Depends(get_db)) -> Program:
    return get_program_(db, program_id)


@api.get('/program', response_model=List[ProgramSchema], responses=extra)
def programs_list(
    db: Session = Depends(get_db), offset: int = 0, limit: int = service_settings.MAX_LIMIT, category: str = None
) -> Union[Response, List[Program]]:
    if limit > service_settings.MAX_LIMIT:
        return Error(f'Maximum limit is {service_settings.MAX_LIMIT}!')
    return get_programs_(db, category).order_by(Program.id).offset(offset).limit(limit).all()


@api.post('/program', response_model=ProgramSchema, responses=extra)
def create_event(
    program: ProgramCreateSchema, db: Session = Depends(get_db)
) -> Union[Response, Program]:
    return create_program_(db=db, program=program)
