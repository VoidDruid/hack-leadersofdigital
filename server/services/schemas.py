from typing import Dict, List, Union

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    ok: bool = False
    error: Union[str, Dict, List] = 'Unknown error'
    error_code: str = 'ERROR'


class ORMModel(BaseModel):  # inherit all models from this one
    class Config:
        orm_mode = True
