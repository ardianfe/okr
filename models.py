import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000), nullable=False)
    okrs = db.relationship('Okr', backref=db.backref('user', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.name

class Okr(db.Model):
    __tablename__ = "okr"
    id = db.Column(db.Integer, primary_key=True)
    objective = db.Column(db.String(200), nullable=False)
    progress = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    okr = db.relationship('KeyResult', backref=db.backref('okr', lazy=True))

    def __repr__(self):
        return '<Okr %r>' % self.objective

class KeyResult(db.Model):
    __tablename__ = "keyresult"
    id = db.Column(db.Integer, primary_key=True)
    indicator = db.Column(db.String(200), nullable=False)
    progress = db.Column(db.Float)
    okr_id = db.Column(db.Integer, db.ForeignKey("okr.id"), nullable=False)
    kr_progress = db.relationship('ProgressKr', lazy='select', backref=db.backref('keyresult', lazy='joined'))


    def __repr__(self):
        return '<KeyResult %r>' % self.indicator



class ProgressKr(db.Model):
    __tablename__ = "progresskr"
    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    progress = db.Column(db.Float, nullable=False)
    kr_id = db.Column(db.Integer, db.ForeignKey("keyresult.id"), nullable=False)

    def __repr__(self):
        return '<ProgressKr %r>' % self.indicator
    
    





