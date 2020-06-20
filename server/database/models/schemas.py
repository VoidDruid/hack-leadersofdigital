import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ORMSchema(BaseModel):
    class Config:
        orm_mode = True


class ParameterCreateSchema(ORMSchema):  # post
    name: str
    type: Optional[str] = 'int'
    weight: Optional[float] = 1
    value: Optional[str] = None


class ParameterSchema(ParameterCreateSchema):  # get
    id: int
    weight: float


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
    name: Optional[str] = None
    description: Optional[str] = None
    hours: Optional[int] = None
    category: Optional[str] = None
    disciplines: Optional[List[int]] = None
    created_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None
    parameters: Optional[List[ParameterSchema]] = None


class ProgramSchema(ProgramCreateSchema):  # get
    id: int
    parameters: List[ParameterSchema]
    disciplines: List[DisciplineSchema]
    rating: Optional[int] = None


class ProgramTemplateCreateSchema(ORMSchema):  # post
    category: str
    hours: Optional[int]
    disciplines: Optional[List[int]] = None


class ProgramTemplateSchema(ProgramTemplateCreateSchema):  # get
    id: int
    disciplines: Optional[List[DisciplineSchema]] = None
