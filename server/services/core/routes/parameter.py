from typing import List, Union

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from conf import service_settings
from crud import get_parameters as get_parameters_
from crud import get_parameter as get_parameter_
from database import Parameter, ParameterSchema
from services.api import Error, extra
from services.dependencies import get_db

from . import api


@api.get('/parameter/{id}', response_model=ParameterSchema)
def get_parameter(parameter_id: int, db: Session = Depends(get_db)) -> Parameter:
    return get_parameter_(db, parameter_id)


@api.get('/parameter', response_model=List[ParameterSchema], responses=extra)
def parameters_list(
    db: Session = Depends(get_db), offset: int = 0, limit: int = service_settings.MAX_LIMIT,
) -> Union[Response, List[Parameter]]:
    if limit > service_settings.MAX_LIMIT:
        return Error(f'Maximum limit is {service_settings.MAX_LIMIT}!')
    return get_parameters_(db).order_by(Parameter.id).offset(offset).limit(limit).all()
