import os
import sqlalchemy as db
from sqlalchemy.orm import Session
from cardda_python import CarddaClient
from models.base import Base
import seed


class BaseWorker:
    def __init__(self) -> None:
        self.cardda_client = CarddaClient(os.environ.get("CARDDA_API_KEY", "dummy_key"))
        self.connect_db()
        self.migrate_db()
        self.seed_db()
        print("-" * 10 + " Setup completed " + "-" * 10)

    @property
    def metadata(self):
        return Base.metadata
    
    def get_session(self):
        return Session(self.engine)
    
    def connect_db(self):
        self.engine = db.create_engine("sqlite+pysqlite:///:memory:", echo=True)
    
    def migrate_db(self):
        self.metadata.create_all(self.engine)
    
    def seed_db(self):
        with self.engine.connect() as conn:
            conn.execute(
                db.insert(Base.metadata.tables['wire_transfers']),
                seed.TRANSACTIONS
            )
            conn.commit()