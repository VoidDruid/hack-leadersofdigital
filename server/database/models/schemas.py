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


class ProgramCreateSchema(ORMSchema):  # post
    name: str
    description: Optional[str] = None
    hours: Optional[int] = None
    is_minor: bool = False
    category: Optional[str] = None


class ProgramSchema(ProgramCreateSchema):  # get
    id: int
    parameters: List[ParameterSchema]
