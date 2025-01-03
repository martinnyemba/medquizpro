#!/usr/bin/env python3
"""Module for the Report model"""
from datetime import datetime
from app import db


class Report(db.Model):
    """Model for user reports of various items"""

    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reported_item_type = db.Column(db.String(50), nullable=False)  # 'quiz', 'question', 'user'
    reported_item_id = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, reviewed, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    reviewed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    resolution_notes = db.Column(db.Text)

    # Relationships
    reporter = db.relationship('User', foreign_keys=[reporter_id], backref='reports_filed')
    reviewer = db.relationship('User', foreign_keys=[reviewed_by_id], backref='reports_reviewed')

    def __repr__(self):
        """
        String representation of the Report object.

        Returns:
            str: A string representation of the Report object.
        """
        return '<Report {}>'.format(self.id)

    def to_dict(self):
        """
        Convert the Report object to a dictionary.

        Returns:
            dict: A dictionary representation of the Report object.
        """
        return {
            'id': self.id,
            'reporter_id': self.reporter_id,
            'reported_item_type': self.reported_item_type,
            'reported_item_id': self.reported_item_id,
            'reason': self.reason,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'reviewed_by_id': self.reviewed_by_id,
            'resolution_notes': self.resolution_notes
        }