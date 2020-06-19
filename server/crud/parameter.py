from sqlalchemy.orm import Query, Session

from database import Parameter


def get_parameters(db: Session,) -> Query:
    return db.query(Parameter)


def get_parameter(db: Session, program_id: int) -> Parameter:
    return db.query(Parameter).filter(Parameter.id == program_id).first()
