from worker.app import app


@app.task()
def scan_programs():
    pass
