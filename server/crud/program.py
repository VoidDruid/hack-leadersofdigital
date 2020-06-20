from typing import Optional

from sqlalchemy.orm import Query, Session

from database.models import Discipline, Parameter, Program, ProgramCreateSchema
from services.api import Error


def get_programs(db: Session, category: Optional[str]) -> Query:
    if category:
        return db.query(Program).filter(Program.category == category)
    else:
        return db.query(Program)


def get_program(db: Session, program_id: int) -> Program:
    return db.query(Program).filter(Program.id == program_id).first()


def create_program(db: Session, program: ProgramCreateSchema) -> Program:
    parameters = db.query(Parameter).all()

    if program.disciplines is None:
        program.disciplines = []

    disciplines = db.query(Discipline).filter(Discipline.id.in_(program.disciplines)).all()

    if len(disciplines) != len(program.disciplines):
        diff = set(program.disciplines) - set([discipline.id for discipline in disciplines])
        raise Error(f'Disciplines with ids {diff} do not exist')

    db_program = Program(**program.dict(exclude={'disciplines', 'parameters'}))

    db_program.rel_parameters.extend(parameters)

    if disciplines:
        db_program.disciplines.extend(disciplines)  # TODO: can be optimized, remove subquery

    db.add(db_program)
    db.commit()
    db.refresh(db_program)

    return db_program


def update_program(db: Session, program_id: int, patch_program: ProgramCreateSchema) -> Program:
    values_dict = patch_program.dict(skip_defaults=True)

    progran_query = db.query(Program).filter(
        Program.id == program_id
    )  # FIXME: make it a single query
    program = progran_query.first()

    db.query(Program).filter(Program.id == program.id).update(values_dict)

    db.commit()
    db.refresh(program)

    return program
