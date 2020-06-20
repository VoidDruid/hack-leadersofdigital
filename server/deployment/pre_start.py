import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from database import Session, Mongo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60  # 1 minute
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        # Check if DB is reachable
        pg = Session()
        pg.execute("SELECT 1")
        mongo = Mongo()
        mongo.list_collections()
    except Exception as e:
        logger.error(e)
        raise e


if __name__ == "__main__":
    init()
