from typing import Optional, List

from sqlalchemy.orm import Query, Session

from database.models import Discipline, Parameter, Program, ProgramCreateSchema
from services.api import Error, NotFoundError


def get_programs(db: Session, category: Optional[str]) -> Query:
    if category:
        return db.query(Program).filter(Program.category == category)
    else:
        return db.query(Program)


def get_program(db: Session, program_id: int) -> Program:
    return db.query(Program).filter(Program.id == program_id).first()


def set_disciplines(db: Session, program: Program, discipline_ids: List[int]):
    if not discipline_ids:
        return

    disciplines = db.query(Discipline).filter(Discipline.id.in_(discipline_ids)).all()

    if len(disciplines) != len(discipline_ids):
        diff = set(discipline_ids) - set([discipline.id for discipline in disciplines])
        raise Error(f'Disciplines with ids {diff} do not exist')

    if disciplines:
        program.disciplines.extend(disciplines)  # TODO: can be optimized, remove subquery


def create_program(db: Session, program: ProgramCreateSchema) -> Program:
    parameters = db.query(Parameter).all()

    if program.disciplines is None:
        program.disciplines = []

    db_program = Program(**program.dict(exclude={'disciplines', 'parameters'}))

    set_disciplines(db, db_program, program.disciplines)

    db_program.rel_parameters.extend(parameters)
    db_program.parameters = program.parameters

    db.add(db_program)
    db.commit()
    db.refresh(db_program)

    return db_program


def update_program(db: Session, program_id: int, patch_program: ProgramCreateSchema) -> Program:
    values_dict = patch_program.dict(skip_defaults=True, exclude={'disciplines', 'parameters'})

    program = db.query(Program).filter(
        Program.id == program_id
    ).one_or_none()

    if not program:
        raise NotFoundError(f'Program <{program_id}> not found')

    set_disciplines(db, program, patch_program.disciplines)
    program.parameters = patch_program.parameters

    if values_dict:
        db.query(Program).filter(Program.id == program.id).update(values_dict)

    db.commit()
    db.refresh(program)

    return program
