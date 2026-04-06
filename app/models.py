from app import db
from datetime import datetime, timezone


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    # Stored consistently in lowercase: "viewer", "analyst", "admin"
    role = db.Column(db.String(20), nullable=False)

    transactions = db.relationship("Transaction", backref="user", lazy=True)


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(100))
    # FIX: datetime.utcnow is deprecated in Python 3.12+; use timezone-aware now()
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    notes = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)