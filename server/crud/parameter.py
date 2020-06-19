from sqlalchemy.orm import Query, Session

from database import Parameter


def get_programs(db: Session,) -> Query:
    return db.query(Parameter)


def get_program(db: Session, program_id: int) -> Parameter:
    return db.query(Parameter).filter(Parameter.id == program_id).first()
