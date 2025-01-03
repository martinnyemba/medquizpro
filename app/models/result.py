#!/usr/bin/env python3
"""Module containing the quiz result model."""
from app import db
from app.models.base import SoftDeleteMixin, TimestampMixin
from app.models.question import Question


class QuizResult(TimestampMixin, SoftDeleteMixin, db.Model):
    """Quiz result model"""
    __tablename__ = 'quiz_results'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    score = db.Column(db.Float)
    time_taken = db.Column(db.Integer)  # in seconds
    completed_at = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='in_progress')
    attempt_number = db.Column(db.Integer, default=1)

    # Detailed results
    answers = db.Column(db.JSON)
    review_notes = db.Column(db.Text)

    def calculate_score(self):
        """
        Calculate score based on answers.

        Returns:
            float: The calculated score as a percentage.
        """
        if not self.answers:
            return 0

        total_points = 0
        earned_points = 0

        for answer in self.answers:
            question = Question.query.get(answer['question_id'])
            if question:
                total_points += question.points
                # Convert both to strings for comparison
                if str(answer['answer']) == str(question.correct_answer):
                    earned_points += question.points
                question.update_stats(str(answer['answer']) == str(question.correct_answer))

        self.score = (earned_points / total_points * 100) if total_points > 0 else 0
        return self.score