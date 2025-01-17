"""Test cases for database models"""
import unittest
from datetime import datetime
from werkzeug.security import generate_password_hash

from app import db
from app.models import User, Quiz, Question, QuestionOption, QuizResult
from tests.test_base import BaseTestCase


class TestModels(BaseTestCase):
    """Test cases for models"""

    def test_user_creation(self):
        """Test user creation and password hashing"""
        user = User(
            first_name='Test',
            last_name='User',
            username='testuser',
            email='test@example.com',
            profession='doctor',
            password_hash=generate_password_hash('password123')
        )
        db.session.add(user)
        db.session.commit()

        retrieved_user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, 'test@example.com')
        self.assertTrue(retrieved_user.check_password('password123'))

    def test_quiz_creation(self):
        """Test quiz creation with questions and options"""
        # Create admin user
        admin = User(
            first_name='Admin',
            last_name='User',
            username='admin',
            email='admin@example.com',
            profession='doctor',
            is_admin=True,
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()

        # Create quiz
        quiz = Quiz(
            title='Test Quiz',
            course='medicine',
            profession='doctor',
            time_limit=15,
            created_by_id=admin.id,
            description='Test quiz description',
            passing_score=60.0
        )
        db.session.add(quiz)
        db.session.commit()

        # Create question and options together
        question = Question(
            quiz_id=quiz.id,
            content='Test question content',
            question_type='multiple_choice',
            created_by_id=admin.id,
            points=1,
            correct_answer=1  # Temporary value, will be updated
        )
        db.session.add(question)
        db.session.flush()  # Get the question ID without committing

        # Create options
        options = []
        for i in range(4):
            option = QuestionOption(
                question_id=question.id,
                content=f'Option {i + 1}',
                is_correct=(i == 0)  # First option is correct
            )
            options.append(option)
            db.session.add(option)

        db.session.flush()  # Get option IDs

        # Update correct answer with the actual option ID
        question.correct_answer = options[0].id
        db.session.commit()

        # Verify quiz creation
        retrieved_quiz = Quiz.query.first()
        self.assertIsNotNone(retrieved_quiz)
        self.assertEqual(retrieved_quiz.title, 'Test Quiz')
        self.assertEqual(retrieved_quiz.questions.count(), 1)

    def test_quiz_result(self):
        """Test quiz result calculation"""
        user = User(
            first_name='Test',
            last_name='User',
            username='testuser',
            email='test@example.com',
            profession='doctor',
            password_hash=generate_password_hash('password123')
        )
        db.session.add(user)
        db.session.commit()

        quiz = Quiz(
            title='Test Quiz',
            course='medicine',
            profession='doctor',
            time_limit=15,
            created_by_id=user.id,
            description='Test quiz description',
            passing_score=60.0
        )
        db.session.add(quiz)
        db.session.commit()

        # Create question with options
        question = Question(
            quiz_id=quiz.id,
            content='Test question',
            question_type='multiple_choice',
            created_by_id=user.id,
            points=1,
            correct_answer=1  # Temporary value, will be updated
        )
        db.session.add(question)
        db.session.flush()  # Get question ID

        option = QuestionOption(
            question_id=question.id,
            content='Correct option',
            is_correct=True
        )
        db.session.add(option)
        db.session.flush()  # Get option ID

        question.correct_answer = option.id
        db.session.commit()

        # Test with correct answer
        result = QuizResult(
            user_id=user.id,
            quiz_id=quiz.id,
            answers=[{'question_id': question.id, 'answer': option.id}],
            time_taken=300,
            status='completed',
            completed_at=datetime.utcnow()
        )
        db.session.add(result)
        db.session.commit()

        score = result.calculate_score()
        self.assertEqual(score, 100.0)


if __name__ == '__main__':
    unittest.main()