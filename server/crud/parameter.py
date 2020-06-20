from sqlalchemy.orm import Query, Session

from database.models import Parameter, ParameterCreateSchema


def get_parameters(db: Session) -> Query:
    return db.query(Parameter)


def get_parameter(db: Session, program_id: int) -> Parameter:
    return db.query(Parameter).filter(Parameter.id == program_id).first()


def create_parameter(db: Session, parameter: ParameterCreateSchema) -> Parameter:
    param = Parameter(**parameter.dict())

    db.add(param)
    db.commit()
    db.refresh(param)

    return param
