from sqlalchemy import ForeignKey
from datetime import datetime as DateTime
from sqlalchemy.orm import mapped_column, Mapped
from .user import User
from core.db import db


class Channel(db.Model):
    __tablename__ = 'Channel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    description = db.Column(db.String(200), nullable=True)
    created_by = db.Column(db.Integer, ForeignKey('User.id'), nullable=True)
    last_modified_by = db.Column(
        db.Integer, ForeignKey('User.id'), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    last_modified_at = db.Column(db.DateTime, nullable=False)