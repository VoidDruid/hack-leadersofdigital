import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    String,
    Table,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from database import Base

ShortString = String(25)
LongString = String(100)


class Config(Base):
    __tablename__ = 'config'
    key = Column(ShortString, primary_key=True, index=True)
    type = Column(ShortString, nullable=False)
    value = Column(LongString, nullable=False)

    def __repr__(self) -> str:
        return f'<Config {self.key}>'


class Parameter(Base):
    __tablename__ = 'parameter'
    id = Column('parameter_id', Integer, primary_key=True, index=True)
    name = Column(ShortString, nullable=False, unique=True)
    type = Column(ShortString, nullable=False)
    weight = Column(Float, nullable=False)
    value = Column(LongString)


class Discipline(Base):
    __tablename__ = 'discipline'
    id = Column('discipline_id', Integer, primary_key=True, index=True)
    name = Column(ShortString, index=True, nullable=False)
    category = Column(ShortString, index=True)
    parameters = Column('parameters', JSONB)


class ConcreteParameter(Base):
    __tablename__ = 'program_to_parameter'
    parameter_id = Column(
        'parameter_id', Integer, ForeignKey(Parameter.id), nullable=False, primary_key=True
    )
    program_id = Column(
        'program_id', Integer, ForeignKey('program.program_id'), nullable=False, primary_key=True
    )
    weight = Column('weight', Float)
    value = Column('value', ShortString)


class ConcreteDiscipline(Base):
    __tablename__ = 'program_to_discipline'
    discipline_id = Column(
        'discipline_id', Integer, ForeignKey(Discipline.id), nullable=False, primary_key=True
    )
    program_id = Column(
        'program_id', Integer, ForeignKey('program.program_id'), nullable=False, primary_key=True
    )
    hours = Column('hours', Integer)


class Program(Base):
    __tablename__ = 'program'
    id = Column('program_id', Integer, primary_key=True, index=True)
    name = Column(ShortString, index=True, nullable=False)
    description = Column(Text)
    hours = Column(Integer)
    category = Column(ShortString, index=True)
    parameters = relationship(Parameter, secondary=ConcreteParameter.__table__)
    disciplines = relationship(Discipline, secondary=ConcreteDiscipline.__table__)

    # time
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True, default=None)


class TemplateDiscipline(Base):
    __tablename__ = 'program_template_to_discipline'
    discipline_id = Column(
        'discipline_id', Integer, ForeignKey(Discipline.id), nullable=False, primary_key=True
    )
    program_id = Column(
        'program_template_id',
        Integer,
        ForeignKey('program_template.program_template_id'),
        nullable=False,
        primary_key=True,
    )
    hours = Column('hours', Integer)


class ProgramTemplate(Base):
    __tablename__ = 'program_template'
    id = Column('program_template_id', Integer, primary_key=True, index=True)
    hours = Column(Integer)
    category = Column(ShortString, unique=True)
    disciplines = relationship(Discipline, secondary=TemplateDiscipline.__table__)
