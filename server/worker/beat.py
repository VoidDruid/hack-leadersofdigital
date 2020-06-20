from .app import app
from .tasks import scan_programs


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30.0, scan_programs.s(), expires=10)
