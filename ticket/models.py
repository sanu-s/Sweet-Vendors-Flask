from datetime import datetime

from app.app import db


class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(20), unique=False, nullable=False)
    status = db.Column(db.String(20), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    modified_by = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return self.name
