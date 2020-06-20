from fastapi import Depends
from sqlalchemy.orm import Session
from services.dependencies import get_pg
from database import Session
from crud import create_parameter, create_discipline
from database.models import ParameterCreateSchema, DisciplineCreateSchema, ProgramCreateSchema
import random

parameters_name = [ 'Востребованность на рынке труда',
                    'Средний уровень капитализации выпускника',
                    'Релевантность транслируемого знания',
                    'Текущий контроль успеваемости',
                    'Промежуточная аттестация',
                    'Показатели научной и инновационной активности',
                    'Использование инновационных образовательных технологий',
                    'Инновационные проекты',
                    'P2P оценка',
                    'Оценка качества преподавания']

categories_name = ['Физика',
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
                   'Алгебра']

pull_names = ['физика', 'химия','алгоритмы', 'структуры', 'данных', 'анализ',
         'прогнозирование', 'регионального', 'рынка',
         'труда', 'ведение', 'переговоров', 'возрастная', 'анатомия',
         'физиология', 'гигиена',
         'деловое', 'русское', 'письмо',
         'информационные', 'коммуникационные', 'технологии', 'в образовательной деятельности']

def populate_parameters():
    db = Session()
    for name in parameters_name:
        param = ParameterCreateSchema(
            name=name,
            type='int',
            weight=random.randint(10, 100),
            value=random.randint(10, 100)
        )
        create_parameter(db, param)

def populate_programs():
    db = Session()



def populate_disciplins():
    db = Session()
    disciplinies_name = []
    for i in range(150):
        disc = DisciplineCreateSchema(
            name=f'{random.choice(pull_names)} {random.choice(pull_names)} {random.choice(pull_names)}',
            category=random.choice(categories_name)
        )
        create_discipline(db, disc)

if __name__ == "__main__":
    populate_disciplins()