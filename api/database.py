from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_app(app):
    db.init_app(app)


def create_db():
    """Creates database"""
    db.create_all()


def drop_db():
    """Drop / Clean database - DANGER ACTION"""
    db.drop_all()

