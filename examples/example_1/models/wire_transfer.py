import sqlalchemy as db
from .base import Base

class WireTransfer(Base):
    __tablename__ = "wire_transfers"

    # common structure in an excel sheet
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Integer)
    commentary = db.Column(db.String(120))
    rut=db.Column(db.String(120))
    email = db.Column(db.String(120))
    account_number = db.Column(db.String(120))
    account_type = db.Column(db.String(120))
    account_bank = db.Column(db.String(120))
    name = db.Column(db.String(120))
    lastname = db.Column(db.String(120))


    def __repr__(self):
        return f"<WireTransfer ${self.amount} to {self.name} {self.lastname}>"