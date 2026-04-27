from database import db
from datetime import datetime


class Article(db.Model):
    __tablename__ = "articles"

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=True)
    url         = db.Column(db.String(500), nullable=False)
    category    = db.Column(db.String(100), nullable=False)
    source      = db.Column(db.String(200), nullable=True)
    published_at = db.Column(db.DateTime, nullable=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):
    __tablename__ = "users"

    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(100), unique=True, nullable=False)
    email      = db.Column(db.String(200), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One user can have many subscriptions
    subscriptions = db.relationship("Subscription", backref="user", lazy=True)


class Subscription(db.Model):
    __tablename__ = "subscriptions"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    topic      = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SearchLog(db.Model):
    __tablename__ = "search_logs"

    id         = db.Column(db.Integer, primary_key=True)
    keyword    = db.Column(db.String(200), nullable=False)
    searched_at = db.Column(db.DateTime, default=datetime.utcnow)
