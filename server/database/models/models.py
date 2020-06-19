from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Table, Text
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


program_to_parameter = Table(
    'program_to_parameter',
    Base.metadata,
    Column('left_id', Integer, ForeignKey(Parameter.id), nullable=False),
    Column('right_id', Integer, ForeignKey('program.program_id'), nullable=False),
    Column('weight', Float),
    Column('value', ShortString),
)


class Program(Base):
    __tablename__ = 'program'
    id = Column('program_id', Integer, primary_key=True, index=True)
    name = Column(ShortString, index=True, nullable=False)
    description = Column(Text)
    hours = Column(Integer)
    is_minor = Column(Boolean, default=False, nullable=False)
    category = Column(ShortString, index=True)
    parameters = relationship(Parameter, secondary=program_to_parameter)
