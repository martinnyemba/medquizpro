#!/usr/bin/env python3
"""Base model classes for the application"""

from datetime import datetime
from app import db


class TimestampMixin:
    """Mixin for adding timestamp fields to models"""
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class SoftDeleteMixin:
    """Mixin for soft delete functionality"""
    deleted_at = db.Column(db.DateTime, nullable=True)
    is_deleted = db.Column(db.Boolean, default=False)

    def soft_delete(self):
        self.deleted_at = datetime.utcnow()
        self.is_deleted = True

    def restore(self):
        self.deleted_at = None
        self.is_deleted = False


class AuditMixin:
    """Mixin for audit trail"""
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    version = db.Column(db.Integer, default=1, nullable=False)
    change_history = db.Column(db.JSON, default=list)

    def log_change(self, user_id, changes):
        if not self.change_history:
            self.change_history = []
        self.change_history.append({
            'version': self.version,
            'user_id': user_id,
            'timestamp': datetime.utcnow().isoformat(),
            'changes': changes
        })
        self.version += 1