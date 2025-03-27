import logging

from sqlmodel import Session

from app.database import engine, init_db, load_models

# This file is run outside of the normal FastAPI environment, so the models need
# to be manually loaded to avoid errors.
load_models()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
