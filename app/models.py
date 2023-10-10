from datetime import datetime, timedelta
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import time
from flask import session, url_for
import base64
import os
import json

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page=page, per_page=per_page,
                                   error_out=False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class User(UserMixin,PaginatedAPIMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    hashed_password = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_teacher = db.Column(db.Boolean, nullable=False, default=False)

    #API token authentication
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)

    question_one = db.relationship('QuestionOne', backref='user', lazy='dynamic')
    question_two = db.relationship('QuestionTwo', backref='subject', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @property
    def password(self):
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self,password):
        self.hashed_password=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.hashed_password,password)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_teacher': self.is_teacher,
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'is_teacher']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    about = db.Column(db.String(200))

    user_id = db.relationship('User', backref='module', lazy='dynamic')
    question_one = db.relationship('QuestionOne', backref='module', lazy='dynamic')
    question_two = db.relationship('QuestionTwo', backref='module', lazy='dynamic')

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'about': self.about,
        }
        return data

    def from_dict(self, data):
        for field in ['name', 'about']:
            if field in data:
                setattr(self, field, data[field])


class Assessments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    is_summative = db.Column(db.Boolean, nullable=False, default=False)
    questions = db.Column(db.String, nullable=False)
    statistics = db.Column(db.String, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class QuestionOne(db.Model, PaginatedAPIMixin):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    difficulty = db.Column(db.Integer, nullable = False)
    total_marks = db.Column(db.Integer, nullable = False)
    num_blanks = db.Column(db.Integer, nullable=False)
    lines = db.Column(db.String, nullable=False)
    answers = db.Column(db.String, nullable=False)
    feedback = db.Column(db.String, nullable=True)
    feedforward = db.Column(db.String, nullable=True)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)

    def to_dict(self):
        data = {
            'id': self.id,
            'question': self.question,
            'difficulty': self.difficulty,
            'total_marks': self.total_marks,
            'num_blanks': self.num_blanks,
            'lines': json.loads(self.lines),
            'answers': json.loads(self.answers),
            'feedback': self.feedback,
            'feedforward': self.feedforward,
            'author_id': self.author_id,
            'module_id': self.module_id
        }
        return data

    def from_dict(self, data):
        for field in ['question', 'difficulty', 'total_marks', 'num_blanks', 'lines', 'answers', 'feedback', 'feedforward', 'author_id', 'module_id']:
            if field in data:
                setattr(self, field, data[field])


class QuestionTwo(db.Model, PaginatedAPIMixin):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200), nullable=False)
    difficulty = db.Column(db.Integer, nullable = False)
    total_marks = db.Column(db.Integer, nullable = False)
    answers = db.Column(db.String, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'), nullable=False)

    def to_dict(self):
        data = {
            'id': self.id,
            'question': self.question,
            'difficulty': self.difficulty,
            'total_marks': self.total_marks,
            'answers': json.loads(self.answers),
            'author_id': self.author_id,
            'module_id': self.module_id
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['question', 'difficulty', 'total_marks', 'answers', 'author_id', 'module_id']:
            if field in data:
                setattr(self, field, data[field])