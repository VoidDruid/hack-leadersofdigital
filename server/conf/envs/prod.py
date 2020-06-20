# For security reasons, should be loaded from env variables in production
PG_NAME = None
PG_USER = None
PG_PASSWORD = None
PG_HOST = None
PG_PORT = '5432'

MONGO_NAME = None
MONGO_USER = None
MONGO_PASSWORD = None
MONGO_HOST = None
MONGO_PORT = '27017'

REDIS_HOST = None
REDIS_PORT = '6379'

CELERY_TASKS_DB = '14'
CELERY_RESULTS_DB = '15'

DEBUG = False
