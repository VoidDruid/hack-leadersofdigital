from typing import Optional

from sqlalchemy.orm import Query, Session

from database.models import Parameter, Program, ProgramCreateSchema


def get_programs(db: Session, category: Optional[str]) -> Query:
    if category:
        return db.query(Program).filter(Program.category == category)
    else:
        return db.query(Program)


def get_program(db: Session, program_id: int) -> Program:
    return db.query(Program).filter(Program.id == program_id).first()


def create_program(db: Session, program: ProgramCreateSchema) -> Program:
    parameters = db.query(Parameter).all()
    db_program = Program(**program.dict(), parameters=parameters)

    db.add(db_program)
    db.commit()
    db.refresh(db_program)

    return db_program
