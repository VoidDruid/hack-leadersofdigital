from typing import Optional

from sqlalchemy.orm import Query, Session

from database.models import Discipline, DisciplineCreateSchema


def get_disciplines(db: Session, category: Optional[str]) -> Query:
    if category:
        return db.query(Discipline).filter(Discipline.category == category)
    else:
        return db.query(Discipline)


def get_discipline(db: Session, id: int) -> Discipline:
    return db.query(Discipline).filter(Discipline.id == id).first()


def create_discipline(db: Session, discipline: DisciplineCreateSchema) -> Discipline:
    new_discipline = Discipline(**discipline.dict())

    db.add(new_discipline)
    db.commit()
    db.refresh(new_discipline)

    return new_discipline
