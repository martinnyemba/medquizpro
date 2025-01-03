#!/usr/bin/env python3
# app/models/submission.py
"""Module for user-submitted questions pending review"""

from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.hybrid import hybrid_property


class QuestionSubmission(db.Model):
    """Model for user-submitted questions pending review"""

    __tablename__ = 'question_submissions'

    id = db.Column(db.Integer, primary_key=True)
    submitter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), default='multiple_choice')
    difficulty_level = db.Column(db.String(20), nullable=False)
    options = db.Column(JSON, nullable=False)  # List of option content
    correct_option_content = db.Column(db.String(500), nullable=False)
    explanation = db.Column(db.Text)
    reference = db.Column(db.String(500))
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    reviewed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationships
    submitter = db.relationship('User', foreign_keys=[submitter_id],
                                backref='submitted_questions')
    reviewer = db.relationship('User', foreign_keys=[reviewed_by_id],
                               backref='reviewed_submissions')

    @hybrid_property
    def correct_option_index(self):
        """
        Get the zero-based index of the correct option.

        Returns:
            int: The index of the correct option, or 0 if not found.
        """
        try:
            return self.options.index(self.correct_option_content)
        except (ValueError, AttributeError):
            return 0

    def get_option_content(self, index):
        """
        Get content of option at specified index.

        Args:
            index (int): The index of the option.

        Returns:
            str: The content of the option at the specified index, or None if not found.
        """
        try:
            return self.options[index]
        except (IndexError, TypeError):
            return None

    def __repr__(self):
        """
        String representation of the QuestionSubmission object.

        Returns:
            str: A string representation of the QuestionSubmission object.
        """
        return f'<QuestionSubmission {self.id}: {self.content[:50]}...>'
