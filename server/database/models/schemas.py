from typing import List, Optional

from pydantic import BaseModel


class ParameterSchema(BaseModel):
    id: int
    name: str
    type: str
    weight: float
    value: Optional[str] = None


class ProgramCreateSchema(BaseModel):  # post
    name: str
    description: Optional[str] = None
    hours: Optional[int] = None
    is_minor: bool = False
    category: Optional[str] = None


class ProgramSchema(ProgramCreateSchema):  # get
    id: int
    parameters: List[ParameterSchema]


class ProgramLightSchema(BaseModel):  # get
    id: int
    name: str