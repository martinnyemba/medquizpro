#!/usr/bin/env python3
"""Module for Model for users"""
from datetime import datetime
from time import time
import jwt
from flask import current_app
from flask_login import UserMixin
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
    """User model with profile features"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    profession = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
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

    @validates('email')
    def validate_email(self, key, value):
        """
        Validate the email address.

        Args:
            key (str): The name of the attribute.
            value (str): The email address to validate.

        Returns:
            str: The validated email address in lowercase.

        Raises:
            ValueError: If the email address is invalid.
        """
        if not value or '@' not in value:
            raise ValueError('Invalid email address')
        return value.lower()

    @property
    def password(self):
        """
        Prevent reading the password attribute.

        Raises:
            AttributeError: Always raised to prevent reading the password.
        """
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        """
        Set the password hash.

        Args:
            password (str): The password to hash.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check if the provided password matches the stored hash.

        Args:
            password (str): The password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        """
        Generate a JWT token for password reset.

        Args:
            expires_in (int): The expiration time in seconds.

        Returns:
            str: The JWT token.
        """
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        """
        Verify the JWT token for password reset.

        Args:
            token (str): The JWT token to verify.

        Returns:
            User: The user associated with the token, or None if invalid.
        """
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.query.get(id)

    @property
    def performance_stats(self):
        """
        Calculate user's overall performance statistics.

        Returns:
            dict: A dictionary containing performance statistics.
        """
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
            'recent_activity': results[-5:]  # Last 5 quizzes
        }


# initializing LoginManager
@login.user_loader
def load_user(user_id):
    """
    User loader callback for Flask-Login.

    Args:
        user_id (int): The ID of the user to load.

    Returns:
        User: The user object, or None if not found.
    """
    return User.query.get(int(user_id))