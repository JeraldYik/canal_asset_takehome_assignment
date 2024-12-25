import atexit
import logging
import signal
import sys
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.service.database.model import *
from src.util.util import singleton

SOURCE_TWITTER = "twitter"
SOURCE_REDDIT = "reddit"


@singleton
class Database:
    def __init__(self):
        self.engine = create_engine("sqlite:///local.db")
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

        def handle_interrupt(sig, frame):
            sys.exit(0)

        def handle_exit():
            self.session.close()
            self.engine.dispose()
            logging.info("Database connection closed & memory cleaned up")

        signal.signal(signal.SIGINT, handle_interrupt)
        atexit.register(handle_exit)

    def bulk_insert(self, data: List[SocialMediaData]):
        try:
            self.session.bulk_save_objects(data)
            self.session.commit()
        except Exception as e:
            logging.error("Database err %s", e)
            self.session.rollback()
        finally:
            logging.info(
                "Table has %s rows", self.session.query(SocialMediaData).count()
            )

    def add_one(self, data: SocialMediaData):
        try:
            self.session.add(data)
            self.session.commit()
        except Exception as e:
            logging.error("Database err %s", e)
            self.session.rollback()
        finally:
            logging.info(
                "Table has %s rows", self.session.query(SocialMediaData).count()
            )


db = Database()
logging.info("Database initialised successfully")


if __name__ == "__main__":
    pass
