import random

import datetime
from fastapi import Depends
from sqlalchemy.orm import Session

from crud import create_discipline, create_parameter, get_disciplines, create_program
from database import Session
from database.models import DisciplineCreateSchema, ParameterCreateSchema, ProgramCreateSchema, Discipline
from services.dependencies import get_pg

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

descriptions='Quo usque tandem abutēre, ' \
             'Catilīna, patientia nostra? quam ' \
             'diu etiam furor iste tuus elūdet? quem' \
             ' ad finem sese effrenāta jactābit audacia? Nihilne' \
             ' te nocturnum praesidium Palatii, nihil urbis vigiliae, ' \
             'nihil timor popŭli, nihil concursus bonōrum omnium, nihil' \
             ' hic munitissĭmus habendi senātus locus. nihil horum ora vultusque ' \
             'movērunt? Patēre tua consilia non sentis? constrictam jam horum omnium ' \
             'scientia tenēri conjuratiōnem tuam non vides? Quid proxĭma, quid superiōre ' \
             'nocte egĕris, ubi fueris, quos convocavĕris, quid consilii cepĕris, quem nostrum' \
             ' ignorāre arbitrāris? 0 tempŏral 0 mores! Senātus haec intellĕgit, consul videt, hic ' \
             'tamen vivit. Vivit? Immo vero etiam in senātum venit, fit publĭci consilii partĭceps, ' \
             'notat et designat ocŭlis ad caedem .unumquemque nostrum: nos autem, fortes viri, satis ' \
             'facĕre rei publĭcae vidēmur, si istīus furōrem ac tela vitēmus. Ad mortem te, Catilīna, duci ' \
             'jussu consŭlis jam pridem oportēbat, in te conferri pestem, quam tu in nos machināris. An vero ' \
             'vir amplissĭmus P. Scipio, pontĭfex maxĭmus, Ti. Gracchum, mediocrĭter labefactantem statum rei' \
             ' publĭcae, privātus interfēcit: Catilīnam, orbem terrae caede atque incendiis vastāre cupientem, ' \
             'nos consŭles perferēmus? Nam illa nimis antīqua praetereo, quod C. Servilius Ahala Spurium Maelium, ' \
             'novis rebus studentem, manu sua occīdit. Fuit, fuit ista quondam in hac re publica virtus, ut viri ' \
             'fortes acriorĭbus suppliciis civem perniciōsum quam acerbissĭmum hostem coërcērent. Habēmus senātus consultum ' \
             'in te, Catilīna, vehĕmens et grave; non deest rei publĭcae consilium neque auctorĭtas hujus ordĭnis: nos, nos, ' \
             'dico aperte, consŭles desŭmus.'

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

'''    name: str
    description: Optional[str] = None
    hours: Optional[int] = None
    category: Optional[str] = None
    disciplines: Optional[List[int]] = None
    created_at: Optional[datetime.datetime] = None
    deleted_at: Optional[datetime.datetime] = None'''

def populate_programs():
    db = Session()
    #create active
    for i in range(30):
        description = ''.join(descriptions.split())
        category = random.choice(categories_name)
        created_at = datetime.datetime.utcnow()
        created_at = created_at.replace(year=created_at.year - random.randint(0,20))
        matched_disciplines = get_disciplines(db, category).all()
        dismatched_disciplines = get_disciplines(db, None).filter(Discipline.category != category).all()

        disciplines = matched_disciplines[0:7] + dismatched_disciplines[0:3]
        program = ProgramCreateSchema(
            name=f'{random.choice(categories_name)} {random.choice(pull_names)}',
            description=description,
            hours=random.randint(100,500),
            category=category,
            created_at=created_at,
            disciplines=[discipline.id for discipline in disciplines]
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
        dismatched_disciplines = get_disciplines(db, None).filter(Discipline.category != category).all()

        disciplines = matched_disciplines[0:7] + dismatched_disciplines[0:3]
        program = ProgramCreateSchema(
            name=f'{random.choice(categories_name)} {random.choice(pull_names)}',
            description=description,
            hours=random.randint(100, 500),
            category=category,
            created_at=created_at,
            deleted_at=deleted_at,
            disciplines=[discipline.id for discipline in disciplines]
        )
        create_program(db, program)


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
    populate_parameters()
    populate_disciplins()
    populate_programs()
