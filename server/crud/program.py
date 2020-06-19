from sqlalchemy.orm import Query, Session
from database import Program

def get_programs(
    db: Session,
) -> Query:
    return db.query(Program)

def get_program(db: Session, program_id: int) -> Program:
    return db.query(Program).filter(Program.id == program_id).first()

