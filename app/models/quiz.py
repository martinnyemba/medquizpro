#!/usr/bin/env python3
"""Module for the Quiz model"""
from datetime import datetime
from sqlalchemy.orm import validates

from app import db
from app.models.base import TimestampMixin, SoftDeleteMixin, AuditMixin
from app.models.result import QuizResult


class Quiz(TimestampMixin, SoftDeleteMixin, AuditMixin, db.Model):
    """Quiz model with additional features"""
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    profession = db.Column(db.String(50), nullable=False)
    difficulty_level = db.Column(db.String(20), default='intermediate')
    time_limit = db.Column(db.Integer, nullable=False)  # in minutes
    passing_score = db.Column(db.Float, default=70.0)
    max_attempts = db.Column(db.Integer, default=5)
    is_published = db.Column(db.Boolean, default=False)
    is_question_bank = db.Column(db.Boolean, default=False)
    requires_approval = db.Column(db.Boolean, default=True)
    approved_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Content and metadata
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    tags = db.Column(db.JSON)
    prerequisites = db.Column(db.JSON)

    # Statistics
    total_attempts = db.Column(db.Integer, default=0)
    average_score = db.Column(db.Float, default=0.0)
    completion_rate = db.Column(db.Float, default=0.0)

    # Relationships
    questions = db.relationship('Question', backref='quiz', lazy='dynamic',
                                cascade='all, delete-orphan')
    results = db.relationship('QuizResult', backref='quiz', lazy='dynamic',
                              cascade='all, delete-orphan')

    @validates('time_limit')
    def validate_time_limit(self, key, value):
        """
        Validate the time limit for the quiz.

        Args:
            key (str): The name of the attribute.
            value (int): The time limit in minutes.

        Returns:
            int: The validated time limit.

        Raises:
            ValueError: If the time limit is less than 5 minutes.
        """
        if value < 5:
            raise ValueError('Time limit must be at least 5 minutes')
        return value

    @property
    def total_questions(self):
        """
        Get the total number of questions in the quiz.

        Returns:
            int: The total number of questions.
        """
        return self.questions.filter_by(is_deleted=False).count()

    def update_statistics(self):
        """
        Update quiz statistics based on results.
        """
        results = self.results.filter_by(is_deleted=False).all()
        if results:
            self.total_attempts = len(results)
            self.average_score = sum(r.score for r in results) / len(results)
            completed = sum(1 for r in results if r.status == 'completed')
            self.completion_rate = (completed / len(results)) * 100

    def get_leaderboard(self, limit=10):
        """
        Get the quiz leaderboard.

        Args:
            limit (int): The number of top results to return.

        Returns:
            list: A list of top quiz results.
        """
        return self.results.filter_by(is_deleted=False) \
            .order_by(QuizResult.score.desc()) \
            .limit(limit).all()