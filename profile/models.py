from datetime import datetime

from app.app import db


class AccountProfile(db.Model):
    __tablename__ = "accountprofiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    phone = db.Column(db.BigInteger, unique=True, nullable=False)
    company = db.Column(db.String(100), unique=False, nullable=False)
    website = db.Column(db.String(120), unique=False, nullable=False)
    address = db.Column(db.String(350), unique=False, nullable=False)
    country = db.Column(db.String(50), unique=False, nullable=False)
    state = db.Column(db.String(80), unique=False, nullable=False)
    district = db.Column(db.String(80), unique=False, nullable=False)
    city = db.Column(db.String(80), unique=False, nullable=False)
    postalcode = db.Column(db.BigInteger, unique=False, nullable=False)
    aadhar = db.Column(db.BigInteger, unique=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    created_by = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return str(self.phone)
