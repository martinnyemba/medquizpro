"""Test cases for admin routes"""
from datetime import datetime
from unittest.mock import patch, MagicMock
from tests.test_base import BaseTestCase
from werkzeug.security import generate_password_hash
from app.models import User, Quiz, Question, QuestionOption, QuizResult
from app import db
import os


class TestAdminRoutes(BaseTestCase):
    """Test cases for admin routes"""

    def setUp(self):
        """Set up test environment before each test"""
        super().setUp()

        # Create test upload directory if it doesn't exist
        os.makedirs(self.app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Create admin user
        self.admin_user = User(
            first_name='Admin',
            last_name='User',
            username='admin',
            email='admin@example.com',
            profession='doctor',
            is_admin=True,
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(self.admin_user)

        # Create regular user
        self.regular_user = User(
            first_name='Regular',
            last_name='User',
            username='user',
            email='user@example.com',
            profession='nurse',
            is_admin=False,
            password_hash=generate_password_hash('user123')
        )
        db.session.add(self.regular_user)

        # Create a test quiz
        self.quiz = Quiz(
            title='Test Quiz',
            course='medicine',
            profession='doctor',
            time_limit=15,
            created_by_id=self.admin_user.id,
            description='Test quiz description',
            passing_score=60.0
        )
        db.session.add(self.quiz)
        db.session.commit()

    def tearDown(self):
        """Clean up after tests"""
        super().tearDown()
        # Clean up test upload directory
        if os.path.exists(self.app.config['UPLOAD_FOLDER']):
            for file in os.listdir(self.app.config['UPLOAD_FOLDER']):
                os.remove(os.path.join(self.app.config['UPLOAD_FOLDER'], file))
            os.rmdir(self.app.config['UPLOAD_FOLDER'])

    def login(self, user):
        """Helper method to log in a user"""
        return self.client.post('/auth/login', data={
            'email': user.email,
            'password': 'admin123' if user.is_admin else 'user123'
        }, follow_redirects=True)

    def test_dashboard_access(self):
        """Test dashboard access control"""
        # Test without login
        response = self.client.get('/admin/dashboard')
        self.assertEqual(response.status_code, 302)  # Redirect to login

        # Test with regular user
        self.login(self.regular_user)
        response = self.client.get('/admin/dashboard')
        self.assertEqual(response.status_code, 302)  # Redirect due to lack of permissions

        # Test with admin user
        self.login(self.admin_user)
        response = self.client.get('/admin/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)

    def test_quiz_management(self):
        """Test quiz management functionality"""
        self.login(self.admin_user)

        # Test quiz list view
        response = self.client.get('/admin/quiz/manage')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Quiz', response.data)

        # Get CSRF token
        csrf_token = response.data.decode().split('csrf_token" value="')[1].split('"')[0]

        # Test quiz creation
        quiz_data = {
            'title': 'New Quiz',
            'description': 'Test Description',
            'course': 'medicine',
            'profession': 'doctor',
            'difficulty_level': 'intermediate',
            'passing_score': 70,
            'time_limit': 30,
            'max_attempts': 3,
            'tags': 'test,quiz',
            'instructions': 'Test instructions',
            'csrf_token': csrf_token
        }
        response = self.client.post('/admin/quiz/create',
                                    data=quiz_data,
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        created_quiz = Quiz.query.filter_by(title='New Quiz').first()
        self.assertIsNotNone(created_quiz)

    def test_question_management(self):
        """Test question management functionality"""
        self.login(self.admin_user)

        # Get CSRF token
        response = self.client.get(f'/admin/quiz/{self.quiz.id}/questions')
        csrf_token = response.data.decode().split('csrf_token" value="')[1].split('"')[0]

        # Create test question with proper setup
        question = Question(
            quiz_id=self.quiz.id,
            content='Test Question',
            question_type='multiple_choice',
            difficulty_level='intermediate',
            points=1,
            created_by_id=self.admin_user.id,
            correct_answer=1  # Temporary value
        )
        db.session.add(question)
        db.session.flush()

        # Create options
        option = QuestionOption(
            question_id=question.id,
            content='Test Option',
            is_correct=True
        )
        db.session.add(option)
        db.session.flush()

        # Update correct answer
        question.correct_answer = option.id
        db.session.commit()

        # Test question creation
        question_data = {
            'content': 'Another Test Question',
            'question_type': 'multiple_choice',
            'difficulty_level': 'intermediate',
            'points': 1,
            'option1': 'Option 1',
            'option2': 'Option 2',
            'option3': 'Option 3',
            'option4': 'Option 4',
            'correct_answer': '1',
            'explanation': 'Test explanation',
            'csrf_token': csrf_token
        }

        response = self.client.post(
            f'/admin/quiz/{self.quiz.id}/questions',
            data=question_data,
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

    @patch('app.routes.admin.send_file')
    def test_export_users(self, mock_send_file):
        """Test user export functionality"""
        self.login(self.admin_user)
        mock_send_file.return_value = 'Mocked file response'
        response = self.client.get('/admin/users/export')
        self.assertEqual(response.status_code, 200)
        mock_send_file.assert_called_once()

    def test_user_management(self):
        """Test user management functionality"""
        self.login(self.admin_user)

        # Test user list view
        response = self.client.get('/admin/users')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Regular User', response.data)

        # Get CSRF token
        csrf_token = response.data.decode().split('csrf_token" value="')[1].split('"')[0]

        # Test user creation
        user_data = {
            'firstname': 'New',
            'lastname': 'User',
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'password2': 'newpass123',
            'profession': 'doctor',
            'is_admin': False,
            'csrf_token': csrf_token
        }
        response = self.client.post('/admin/users/create',
                                    data=user_data,
                                    follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        created_user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(created_user)