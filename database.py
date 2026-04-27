from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy database object
# This will be imported by both app.py and models.py
db = SQLAlchemy()


def init_db(app):
    """Connect the database to the Flask app."""
    db.init_app(app)

    with app.app_context():
        # Import models so SQLAlchemy knows about the tables
        from models import Article, User, Subscription, SearchLog

        # Create all tables if they don't exist yet
        db.create_all()
