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


class DisciplineSchema(ORMSchema):
    id: int
    name: str
    category: str


class ProgramCreateSchema(ORMSchema):  # post
    name: str
    description: Optional[str] = None
    hours: Optional[int] = None
    category: Optional[str] = None
    disciplines: Optional[List[int]] = None
    created_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None


class ProgramSchema(ProgramCreateSchema):  # get
    id: int
    parameters: List[ParameterSchema]
    disciplines: List[DisciplineSchema]
