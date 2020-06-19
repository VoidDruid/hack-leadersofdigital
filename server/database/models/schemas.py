import datetime
from typing import List, Optional

from pydantic import BaseModel


class ORMSchema(BaseModel):
    class Config:
        orm_mode = True


class ParameterSchema(ORMSchema):
    id: int
    name: str
    type: str
    weight: float
    value: Optional[str] = None
    created_at: datetime.datetime
    deleted_at: Optional[datetime.datetime]


class ProgramCreateSchema(ORMSchema):  # post
    name: str
    description: Optional[str] = None
    hours: Optional[int] = None
    is_minor: bool = False
    category: Optional[str] = None
    created_at: Optional[datetime.datetime]
    deleted_at: Optional[datetime.datetime]


class ProgramSchema(ProgramCreateSchema):  # get
    id: int
    parameters: List[ParameterSchema]
