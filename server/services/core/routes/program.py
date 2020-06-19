from typing import List, Union

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from conf import service_settings
from crud import get_program as get_program_
from crud import get_programs as get_programs_
from database import Program, ProgramModel, ProgramModelLight
from services.api import Error, responses
from services.dependencies import get_db

from . import api


@api.get('/program/{id}', response_model=ProgramModel)
def get_program(id: int, db: Session = Depends(get_db)) -> Program:
    return get_program_(db, id)


@api.get('/program', response_model=List[ProgramModelLight], responses=responses)
def programs_list(
    db: Session = Depends(get_db), offset: int = 0, limit: int = service_settings.MAX_LIMIT,
) -> Union[Response, List[Program]]:
    if limit > service_settings.MAX_LIMIT:
        return Error(f'Maximum limit is {service_settings.MAX_LIMIT}!')
    programs = get_programs_(db).order_by(Program.id).offset(offset).limit(limit).all()
    my_programs = List[ProgramModelLight]
    for p in programs:
        my_programs.append({'name': p['name'], 'id': p['id']})
