from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
import secrets
from app import db
from app.models.base import TimestampMixin, SoftDeleteMixin


class UserSession(UserMixin, TimestampMixin, SoftDeleteMixin, db.Model):
    """
    User Session Model for handling authentication sessions and JWT tokens.
    Includes security features and session management capabilities.
    """
    __tablename__ = 'user_sessions'

    # Constants
    TOKEN_LENGTH = 64
    SESSION_DURATION = timedelta(days=30)
    REFRESH_THRESHOLD = timedelta(hours=1)

    # Core fields
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token = db.Column(db.String(512), unique=True, nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    device_info = db.Column(db.JSON, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)  # IPv6 compatible
    is_revoked = db.Column(db.Boolean, default=False, nullable=False)
    last_accessed_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # List of attributes to delegate to User model
    USER_ATTRIBUTES = [
        'profession', 'is_active', 'is_admin', 'email', 'username',
        'first_name', 'last_name', 'profile_image', 'specialization',
        'experience_years', 'institution', 'bio', 'display_name',
        'performance_stats', 'achievements', 'quiz_results', 'created_quizzes',
        'study_groups'  # Adding all relationship attributes
    ]

    def __init__(self, user_id: int, device_info: Dict[str, Any] = None, ip_address: str = None):
        """Initialize a new user session with secure defaults."""
        super().__init__()
        self.user_id = user_id
        self.device_info = device_info or {}
        self.ip_address = ip_address
        self.refresh_token()

    def __getattr__(self, name):
        """
        Delegate attribute access to User model for specified attributes.
        This is called when an attribute is not found on the UserSession instance.
        """
        if name in self.USER_ATTRIBUTES:
            if self.user is not None:
                return getattr(self.user, name)
        raise AttributeError(f"'UserSession' object has no attribute '{name}'")

    def get_id(self):
        """Required method for Flask-Login."""
        return f's_{self.id}'

    def refresh_token(self) -> None:
        """Generate a new secure token and update expiration."""
        self.token = secrets.token_urlsafe(self.TOKEN_LENGTH)
        self.expires_at = datetime.utcnow() + self.SESSION_DURATION
        self.is_revoked = False

    @validates('ip_address')
    def validate_ip_address(self, key, ip_address):
        """Validate IP address format."""
        if ip_address and len(ip_address) > 45:  # Max length for IPv6
            raise ValueError("Invalid IP address format")
        return ip_address

    @hybrid_property
    def is_active(self) -> bool:
        """Check if the session is currently active."""
        return (
                not self.is_deleted
                and not self.is_revoked
                and self.expires_at > datetime.utcnow()
                and self.user is not None
                and self.user.is_active
        )

    @hybrid_property
    def needs_refresh(self) -> bool:
        """Check if the session token needs to be refreshed."""
        return (
                self.is_active and
                self.expires_at - datetime.utcnow() < self.REFRESH_THRESHOLD
        )

    def revoke(self) -> None:
        """Revoke the current session."""
        self.is_revoked = True
        db.session.commit()

    def update_last_accessed(self) -> None:
        """Update the last accessed timestamp."""
        self.last_accessed_at = datetime.utcnow()
        db.session.commit()

    @classmethod
    def cleanup_expired(cls) -> int:
        """Remove expired and revoked sessions."""
        result = cls.query.filter(
            (cls.expires_at < datetime.utcnow()) |
            (cls.is_revoked == True)
        ).delete()
        db.session.commit()
        return result

    @classmethod
    def get_active_sessions(cls, user_id: int) -> list:
        """Get all active sessions for a user."""
        return cls.query.filter_by(
            user_id=user_id,
            is_revoked=False,
            is_deleted=False
        ).filter(cls.expires_at > datetime.utcnow()).all()

    def __repr__(self) -> str:
        return f'<UserSession {self.id} (User: {self.user_id})>'