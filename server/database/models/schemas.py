import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ORMSchema(BaseModel):
    class Config:
        orm_mode = True


class ParameterSchema(ORMSchema):  # get
    id: int
    name: str
    type: str
    weight: float
    value: Optional[str] = None


class DisciplineBaseSchema(ORMSchema):
    name: str
    category: str


class DisciplineCreateSchema(DisciplineBaseSchema):  # post
    parameters: Optional[Dict[str, Any]]


class DisciplineSchema(DisciplineBaseSchema):  # get list
    id: int


class DisciplineFullSchema(DisciplineCreateSchema):  # get one
    id: int


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


class ProgramTemplateCreateSchema(ORMSchema):  # post
    category: str
    hours: Optional[int]
    disciplines: Optional[List[int]] = None


class ProgramTemplateSchema(ProgramTemplateCreateSchema):  # get
    id: int
    disciplines: Optional[List[DisciplineSchema]] = None
