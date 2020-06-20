from celery import Celery

from conf import redis_settings

redis_base_conn = f'redis://{redis_settings.REDIS_HOST}:{redis_settings.REDIS_PORT}'

app = Celery(
    'worker',
    broker=f'{redis_base_conn}/{redis_settings.CELERY_TASKS_DB}',
    result_backend=f'{redis_base_conn}/{redis_settings.CELERY_RESULT_DB}',
)
app.conf.broker_transport_options = {
    'visibility_timeout': 60*15  # 15 minutes
}

from .tasks import *  # isort: ignore
