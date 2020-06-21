import datetime
import random

from sqlalchemy.orm import Session

from crud import create_discipline, create_parameter, create_program, get_disciplines
from database import Session
from database.models import (
    Discipline,
    DisciplineCreateSchema,
    ParameterCreateSchema,
    ProgramCreateSchema,
)

parameters_name = [
    'Востребованность на рынке труда',
    'Средний уровень капитализации выпускника',
    'Релевантность транслируемого знания',
    'Текущий контроль успеваемости',
    'Промежуточная аттестация',
    'Показатели научной и инновационной активности',
    'Использование инновационных образовательных технологий',
    'Инновационные проекты',
    'P2P оценка',
    'Оценка качества преподавания',
]

categories_name = [
    'Физика',
    'Математика',
    'Биология',
    'Медицина',
    'Информатика',
    'Экология',
    'Экономика',
    'Химия',
    'Социология',
    'Лингвистика',
    'Филология',
    'Философия',
    'Риторика',
    'Программирование',
    'Политология',
    'Правоведение',
    'Культурология',
    'Геополитика',
    'Алгебра',
]

pull_names = [
    'физика',
    'химия',
    'алгоритмы',
    'структуры',
    'данных',
    'анализ',
    'прогнозирование',
    'регионального',
    'рынка',
    'труда',
    'ведение',
    'переговоров',
    'возрастная',
    'анатомия',
    'физиология',
    'гигиена',
    'деловое',
    'русское',
    'письмо',
    'информационные',
    'коммуникационные',
    'технологии',
    'в образовательной деятельности',
]

descriptions = (
    'Quo usque tandem abutēre, '
    'Catilīna, patientia nostra? quam '
    'diu etiam furor iste tuus elūdet? quem'
    ' ad finem sese effrenāta jactābit audacia? Nihilne'
    ' te nocturnum praesidium Palatii, nihil urbis vigiliae, '
    'nihil timor popŭli, nihil concursus bonōrum omnium, nihil'
    ' hic munitissĭmus habendi senātus locus. nihil horum ora vultusque '
    'movērunt? Patēre tua consilia non sentis? constrictam jam horum omnium '
    'scientia tenēri conjuratiōnem tuam non vides? Quid proxĭma, quid superiōre '
    'nocte egĕris, ubi fueris, quos convocavĕris, quid consilii cepĕris, quem nostrum'
)


def populate_parameters():
    db = Session()
    for name in parameters_name:
        param = ParameterCreateSchema(
            name=name, type='int', weight=random.randint(10, 100), value=random.randint(10, 100)
        )
        create_parameter(db, param)


def populate_programs():
    db = Session()
    # create active
    for i in range(30):
        description = descriptions
        category = random.choice(categories_name)
        created_at = datetime.datetime.utcnow()
        created_at = created_at.replace(year=created_at.year - random.randint(0, 20))

        matched_disciplines = get_disciplines(db, category).all()
        dismatched_disciplines = (
            get_disciplines(db, None).filter(Discipline.category != category).all()
        )

        disciplines = set(
                random.choices(matched_disciplines, k=random.randint(5, 7))
                +
                random.choices(dismatched_disciplines, k=random.randint(1, 4))
        )

        program = ProgramCreateSchema(
            name=f'{random.choice(categories_name)} {random.choice(pull_names)}',
            description=description,
            hours=random.randint(100, 500),
            category=category,
            created_at=created_at,
            disciplines=[discipline.id for discipline in disciplines],
        )
        create_program(db, program)
    # create inactive
    for i in range(30):
        description = ''.join(descriptions.split())
        category = random.choice(categories_name)

        created_at = datetime.datetime.utcnow()
        created_at = created_at.replace(year=created_at.year - random.randint(10, 20))

        deleted_at = created_at
        deleted_at = deleted_at.replace(year=deleted_at.year + 1)

        matched_disciplines = get_disciplines(db, category).all()
        dismatched_disciplines = (
            get_disciplines(db, None).filter(Discipline.category != category).all()
        )

        disciplines = matched_disciplines[0:7] + dismatched_disciplines[0:3]
        program = ProgramCreateSchema(
            name=f'{random.choice(categories_name)} {random.choice(pull_names)}',
            description=description,
            hours=random.randint(100, 500),
            category=category,
            created_at=created_at,
            deleted_at=deleted_at,
            disciplines=[discipline.id for discipline in disciplines],
        )
        create_program(db, program)


def populate_disciplins():
    db = Session()
    for i in range(150):
        disc = DisciplineCreateSchema(
            name=f'{random.choice(pull_names)} {random.choice(pull_names)} {random.choice(pull_names)}',
            category=random.choice(categories_name),
        )
        create_discipline(db, disc)


if __name__ == '__main__':
    populate_parameters()
    populate_disciplins()
    populate_programs()
