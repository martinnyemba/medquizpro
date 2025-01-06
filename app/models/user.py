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
from app.models.user_session import UserSession


class UserAchievement(db.Model):
    """Model for user achievements and badges"""
    __tablename__ = 'user_achievements'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    achievement_type = db.Column(db.String(50), nullable=False)
    achievement_data = db.Column(db.JSON)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, TimestampMixin, SoftDeleteMixin, db.Model):
    """User model with profile and session management features"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    username = db.Column(db.String(120), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    profession = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)
    last_ip_address = db.Column(db.String(45))  # Added for session tracking
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

    # Regular sessions relationship
    sessions = db.relationship(
        'UserSession',
        backref=db.backref('user', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    # Active sessions relationship with overlaps
    active_sessions = db.relationship(
        'UserSession',
        primaryjoin='and_(User.id == UserSession.user_id, '
                    'UserSession.is_deleted == False, '
                    'UserSession.is_revoked == False, '
                    'UserSession.expires_at > func.now())',
        backref=db.backref('active_user', lazy='joined'),
        lazy='dynamic',
        overlaps="sessions,user"
    )

    def create_session(self, device_info=None, ip_address=None):
        """
        Create a new session for the user.

        Args:
            device_info (dict): Information about the device
            ip_address (str): IP address of the client

        Returns:
            UserSession: The newly created session
        """
        from app.models.user_session import UserSession  # Import here to avoid circular import

        session = UserSession(
            user_id=self.id,
            device_info=device_info,
            ip_address=ip_address
        )
        self.last_ip_address = ip_address
        self.last_login = datetime.utcnow()

        db.session.add(session)
        db.session.commit()
        return session

    def revoke_all_sessions(self, except_session_id=None):
        """
        Revoke all active sessions for the user.

        Args:
            except_session_id (int): Optional session ID to keep active

        Returns:
            int: Number of sessions revoked
        """
        query = self.active_sessions
        if except_session_id is not None:
            query = query.filter(UserSession.id != except_session_id)

        sessions = query.all()
        for session in sessions:
            session.revoke()

        return len(sessions)

    @hybrid_property
    def has_active_session(self):
        """Check if user has any active sessions."""
        return self.active_sessions.count() > 0

    # Existing methods remain unchanged
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


# Update the user loader to handle both User and UserSession
@login.user_loader
def load_user(id_str):
    """
    Enhanced user loader callback for Flask-Login.
    Handles both User and UserSession IDs.

    Args:
        id_str (str): The ID string, which could be either a user ID
                     or a session ID prefixed with 's_'

    Returns:
        Union[User, UserSession]: The user or session object, or None if not found
    """
    try:
        if isinstance(id_str, str) and id_str.startswith('s_'):
            from app.models.user_session import UserSession
            session_id = int(id_str[2:])
            session = UserSession.query.filter_by(
                id=session_id,
                is_revoked=False,
                is_deleted=False
            ).filter(UserSession.expires_at > datetime.utcnow()).first()

            if session:
                session.update_last_accessed()
                return session

        return User.query.get(int(id_str))
    except (ValueError, AttributeError):
        return None