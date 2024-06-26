# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import DeclarativeBase, Session
# from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from celery import Celery

db = SQLAlchemy(session_options= {
    "expire_on_commit": False
}
)
test_db = SQLAlchemy()

redis = Redis(host='localhost', port=6379,decode_responses=True)

def get_db():
    """
    Returns the database object.

    If the database is not initialized, it raises an exception.
    """
    return db

def get_session():
    """Returns a session object bound to the engine"""
    return db.session


def get_test_session():
    """Returns a session object bound to the test engine"""
    return test_db.session

def get_redis():
    """Returns the redis object"""
    return redis

def create_celery_inst(app):
    celery = Celery(app.import_name)
    celery.conf.update(
        broker_url='redis://localhost:6379/1',
        result_backend='redis://localhost:6379/2',
        timezone='Asia/Kolkata'
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
     
    return celery

