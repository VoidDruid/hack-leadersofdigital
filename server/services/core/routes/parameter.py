from typing import List, Union

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from conf import service_settings
from crud import get_parameter as get_parameter_
from crud import get_parameters as get_parameters_
from database import Parameter, ParameterSchema
from services.api import extra
from services.dependencies import get_db
from services.utils import paginate

from . import api


@api.get('/parameter/{id}', response_model=ParameterSchema)
def get_parameter(parameter_id: int, db: Session = Depends(get_db)) -> Parameter:
    return get_parameter_(db, parameter_id)


@api.get('/parameter', response_model=List[ParameterSchema], responses=extra)
def parameters_list(
    db: Session = Depends(get_db), offset: int = 0, limit: int = service_settings.MAX_LIMIT,
) -> Union[Response, List[Parameter]]:
    return paginate(get_parameters_(db), Parameter, offset, limit)
