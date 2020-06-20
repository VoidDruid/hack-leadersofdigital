from worker.app import app

from database import Session, Mongo


@app.task()
def scan_programs():
    pass
