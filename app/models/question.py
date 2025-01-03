#!/usr/bin/env python3
"""Module for the Question model"""

from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.models.base import TimestampMixin, SoftDeleteMixin, AuditMixin


class QuestionTag(TimestampMixin, db.Model):
    """Model for question tags"""
    __tablename__ = 'question_tags'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    tag_name = db.Column(db.String(50), nullable=False)
    tag_type = db.Column(db.String(30))


class Question(TimestampMixin, SoftDeleteMixin, AuditMixin, db.Model):
    """Enhanced question model"""
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), default='multiple_choice')
    difficulty_level = db.Column(db.String(20), default='intermediate')
    correct_answer = db.Column(db.Integer, nullable=False)  # Changed to Integer
    explanation = db.Column(db.Text)
    points = db.Column(db.Integer, default=1)

    # Media content
    image_url = db.Column(db.String(500))
    video_url = db.Column(db.String(500))

    # Statistics
    times_answered = db.Column(db.Integer, default=0)
    times_correct = db.Column(db.Integer, default=0)

    # Relationships
    options = db.relationship('QuestionOption', backref='question', lazy='dynamic',
                              cascade='all, delete-orphan')
    tags = db.relationship('QuestionTag', backref='question', lazy='dynamic',
                           cascade='all, delete-orphan')

    def check_answer(self, submitted_answer):
        """
        Check if the submitted answer is correct.

        Args:
            submitted_answer (int or str): The answer submitted by the user.

        Returns:
            bool: True if the answer is correct, False otherwise.
        """
        try:
            # Convert both to integers for comparison
            return int(submitted_answer) == int(self.correct_answer)
        except (ValueError, TypeError):
            return False

    def get_correct_option(self):
        """
        Get the correct option object.

        Returns:
            QuestionOption: The correct option object.
        """
        return QuestionOption.query.get(self.correct_answer)

    @hybrid_property
    def success_rate(self):
        """
        Calculate the success rate of the question.

        Returns:
            float: The success rate as a percentage.
        """
        if self.times_answered == 0:
            return 0
        return (self.times_correct / self.times_answered) * 100

    def update_stats(self, is_correct):
        """
        Update question statistics.

        Args:
            is_correct (bool): Whether the submitted answer was correct.
        """
        self.times_answered += 1
        if is_correct:
            self.times_correct += 1


class QuestionOption(TimestampMixin, db.Model):
    """Enhanced question option model"""
    __tablename__ = 'question_options'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    explanation = db.Column(db.Text)