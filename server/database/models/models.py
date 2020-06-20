import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import object_session, relationship

from database import Base

ShortString = String(50)
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
    name = Column(String(100), nullable=False, unique=True)
    type = Column(ShortString, nullable=False)
    weight = Column(Float, nullable=False)
    value = Column(LongString)


class Discipline(Base):
    __tablename__ = 'discipline'
    id = Column('discipline_id', Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
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
    name = Column(String(100), index=True, nullable=False)
    description = Column(Text)
    hours = Column(Integer)
    category = Column(ShortString, index=True)
    rating = Column(Integer)
    rel_parameters = relationship(Parameter, secondary=ConcreteParameter.__table__)
    disciplines = relationship(Discipline, secondary=ConcreteDiscipline.__table__)

    @property
    def parameters(self):
        joined_params = (
            object_session(self)
            .query(Parameter, ConcreteParameter)
            .filter(ConcreteParameter.program_id == self.id)
            .filter(Parameter.id == ConcreteParameter.parameter_id)
            .all()
        )

        params = []
        for (param, concrete_param) in joined_params:
            param_dict = {'id': param.id, 'type': param.type, 'name': param.name}

            if concrete_param.weight is not None:
                param_dict['weight'] = concrete_param.weight
            else:
                param_dict['weight'] = param.weight

            if concrete_param.value is not None:
                param_dict['value'] = concrete_param.value
            else:
                param_dict['value'] = param.value

            params.append(param_dict)

        return params

    # time
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
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
