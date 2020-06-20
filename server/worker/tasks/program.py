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

    processing = state_db.find_one({'key': PROCESS_KEY})
    if processing:
        to_process = set(not_rated_programs) - set(processing['planned'])
        state_db.update_one(
            {'_id': processing['_id']}, {'$set': {'key': PROCESS_KEY, 'planned': to_process}}
        )
    else:
        to_process = not_rated_programs
        state_db.insert_one({'key': PROCESS_KEY, 'planned': to_process})

    return to_process


@app.task()
def process_program(id: int) -> Optional[int]:
    session = Session()
    stats_db = Mongo(STATS_COLL)

    program = session.query(Program).filter(Program.id == id).one_or_none()
    if not program:
        return

    parameters = program.parameters

    score = 0
    for param in parameters:
        score += param['weight'] * param['value']

    program.score = score

    return score
