from typing import List, Union

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from conf import service_settings
from crud import get_program as get_program_
from crud import get_programs as get_programs_
from database import Program, ProgramSchema, ProgramLightSchema
from services.api import Error, extra
from services.dependencies import get_db

from . import api


@api.get('/program/{id}', response_model=ProgramSchema)
def get_program(program_id: int, db: Session = Depends(get_db)) -> Program:
    return get_program_(db, program_id)


@api.get('/program', response_model=List[ProgramLightSchema], responses=extra)
def programs_list(
    db: Session = Depends(get_db), offset: int = 0, limit: int = service_settings.MAX_LIMIT,
) -> Union[Response, List[Program]]:
    if limit > service_settings.MAX_LIMIT:
        return Error(f'Maximum limit is {service_settings.MAX_LIMIT}!')
    programs = get_programs_(db).order_by(Program.id).offset(offset).limit(limit).all()
    my_programs = List[ProgramLightSchema]
    for p in programs:
        my_programs.append({'name': p['name'], 'id': p['id']})
