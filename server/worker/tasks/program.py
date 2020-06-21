from typing import List, Optional

from worker.app import app

from database import Mongo, Session
from database.models import Program

STATE_COLL = 'state'
STATS_COLL = 'stats'
PROCESS_KEY = 'processing'


@app.task()
def scan_programs() -> List[int]:
    session = Session()
    state_db = Mongo(STATE_COLL)

    not_rated_programs = [
        prog_id for (prog_id,) in session.query(Program.id).filter(Program.rating.is_(None))
    ]

    if not not_rated_programs:
        return []

    processing = state_db.find_one({'key': PROCESS_KEY})
    if processing:
        to_process = list(set(not_rated_programs) - set(processing['planned']))
        state_db.update_one(
            {'_id': processing['_id']},
            {'$set': {'key': PROCESS_KEY, 'planned': processing['planned'] + to_process}}
        )
    else:
        to_process = not_rated_programs
        state_db.insert_one({'key': PROCESS_KEY, 'planned': to_process})

    for program_id in to_process:
        process_program.delay(program_id)

    return to_process


@app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_jitter=True)
def process_program(self, id: int) -> Optional[str]:
    session = Session()

    program = session.query(Program).filter(Program.id == id).one_or_none()
    if not program:
        return

    state_db = Mongo(STATE_COLL)

    parameters = program.parameters

    rating = 0
    for param in parameters:
        rating += param['weight'] * int(param['value'])  # TODO: type processing
    program.rating = int(rating)  # round score

    session.add(program)
    session.commit()

    state_db.update_one(
        {'key': PROCESS_KEY},
        {'$pull': {'planned': id}}
    )

    stats_db = Mongo(STATS_COLL)

    return f'New rating for program <{id}>: {rating}'
