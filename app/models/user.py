#!/usr/bin/env python3
"""Module for Model for users"""
from datetime import datetime
from time import time
import jwt
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login
from app.models.base import TimestampMixin, SoftDeleteMixin


class UserAchievement(db.Model):
    """Model for user achievements and badges"""
    __tablename__ = 'user_achievements'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    achievement_type = db.Column(db.String(50), nullable=False)
    achievement_data = db.Column(db.JSON)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, TimestampMixin, SoftDeleteMixin, db.Model):
    """User model with profile management features"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    profession = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    last_ip_address = db.Column(db.String(45))
    profile_image = db.Column(db.String(256))
    specialization = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)
    institution = db.Column(db.String(300))
    bio = db.Column(db.Text)

    # Relationships
    quiz_results = db.relationship('QuizResult', backref='user', lazy='dynamic')
    created_quizzes = db.relationship('Quiz', backref='creator', lazy='dynamic',
                                    foreign_keys='Quiz.created_by_id')
    achievements = db.relationship('UserAchievement', backref='user', lazy='dynamic')
    study_groups = db.relationship('StudyGroup', secondary='user_study_groups',
                                 backref=db.backref('members', lazy='dynamic'))

    def verify_update(self):
        """Verify that changes have been persisted to the database"""
        db.session.refresh(self)
        return True

    def get_id(self):
        """Return the user id as a string"""
        return str(self.id)

    def update_last_login(self, ip_address=None):
        """Update last login time and IP address"""
        self.last_login = datetime.utcnow()
        if ip_address:
            self.last_ip_address = ip_address
        db.session.commit()

    @validates('email')
    def validate_email(self, key, value):
        if not value or '@' not in value:
            raise ValueError('Invalid email address')
        return value.lower()

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                          algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.query.get(id)

    def display_name(self) -> str:
        if not self.email and not self.first_name and not self.last_name:
            return ""
        if not self.first_name and not self.last_name:
            return self.email
        if not self.last_name:
            return self.first_name
        if not self.first_name:
            return self.last_name
        return f"{self.first_name} {self.last_name}"

    @property
    def performance_stats(self):
        """Get performance statistics for the user"""
        results = self.quiz_results.filter_by(is_deleted=False).all()
        if not results:
            return {
                'average_score': 0,
                'quizzes_taken': 0,
                'highest_score': 0,
                'lowest_score': 0,
                'recent_activity': []
            }

        scores = [result.score for result in results if result.score is not None]
        if not scores:
            return {
                'average_score': 0,
                'quizzes_taken': len(results),
                'highest_score': 0,
                'lowest_score': 0,
                'recent_activity': results[-5:]
            }

        return {
            'average_score': sum(scores) / len(scores),
            'quizzes_taken': len(results),
            'highest_score': max(scores),
            'lowest_score': min(scores),
            'recent_activity': results[-5:]
        }


@login.user_loader
def load_user(user_id):
    """User loader function with legacy session ID handling"""
    try:
        # legacy session IDs that start with 's_'
        if isinstance(user_id, str) and user_id.startswith('s_'):
            user_id = user_id[2:]
        return User.query.get(int(user_id))
    except (ValueError, AttributeError):
        return None