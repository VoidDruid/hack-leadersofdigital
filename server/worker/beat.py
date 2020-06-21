from .app import app
from .tasks import scan_programs

from conf import service_settings


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        service_settings.SCAN_PROGRAMS_DELAY,
        scan_programs.s(),
        expires=10
    )
