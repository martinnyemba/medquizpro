"""Test cases for forms and form validation"""
from tests.test_base import BaseTestCase
from app.forms import (LoginForm, RegistrationForm, QuizForm, QuestionForm,
                       ProfileForm, ResetPasswordForm, ContactForm)
from io import BytesIO
from werkzeug.datastructures import FileStorage


class TestLoginForm(BaseTestCase):
    """Test cases for login form"""

    def test_valid_login_form(self):
        """Test login form with valid data"""
        form = LoginForm(formdata=None)
        form.email.data = "test@example.com"
        form.password.data = "password123"
        self.assertTrue(form.validate())

    def test_invalid_email_format(self):
        """Test login form with invalid email format"""
        form = LoginForm(formdata=None)
        form.email.data = "invalid-email"
        form.password.data = "password123"
        self.assertFalse(form.validate())
        self.assertIn("Please enter a valid email address", form.email.errors)

    def test_password_length(self):
        """Test password length validation"""
        form = LoginForm(formdata=None)
        form.email.data = "test@example.com"
        form.password.data = "short"  # Less than 8 characters
        self.assertFalse(form.validate())
        self.assertIn("Password must be at least 8 characters long", form.password.errors)


class TestRegistrationForm(BaseTestCase):
    """Test cases for registration form"""

    def test_valid_registration(self):
        """Test registration form with valid data"""
        form = RegistrationForm(formdata=None)
        form.firstname.data = "John"
        form.lastname.data = "Doe"
        form.username.data = "johndoe"
        form.email.data = "john@example.com"
        form.password.data = "password123"
        form.password2.data = "password123"
        form.profession.data = "doctor"
        self.assertTrue(form.validate())

    def test_password_match(self):
        """Test password confirmation matching"""
        form = RegistrationForm(formdata=None)
        form.firstname.data = "John"
        form.lastname.data = "Doe"
        form.username.data = "johndoe"
        form.email.data = "john@example.com"
        form.password.data = "password123"
        form.password2.data = "different123"
        form.profession.data = "doctor"
        self.assertFalse(form.validate())

    def test_invalid_username(self):
        """Test username format validation"""
        form = RegistrationForm(formdata=None)
        form.firstname.data = "John"
        form.lastname.data = "Doe"
        form.username.data = "john@doe"  # Invalid character
        form.email.data = "john@example.com"
        form.password.data = "password123"
        form.password2.data = "password123"
        form.profession.data = "doctor"
        self.assertFalse(form.validate())
        self.assertIn("Username can only contain letters, numbers, and dots.",
                      form.username.errors)


class TestQuestionForm(BaseTestCase):
    """Test cases for question form"""

    def test_duplicate_options(self):
        """Test validation of duplicate options"""
        form = QuestionForm(formdata=None)
        form.content.data = "Test question"
        form.question_type.data = "multiple_choice"
        form.difficulty_level.data = "intermediate"
        form.points.data = 1
        form.option1.data = "Same Answer"
        form.option2.data = "Same Answer"  # Duplicate
        form.option3.data = "Option 3"
        form.option4.data = "Option 4"
        form.correct_answer.data = "1"

        # Test validate() method which includes validate_options()
        self.assertFalse(form.validate())
        self.assertIn('All options must be unique', form.option1.errors)


class TestProfileForm(BaseTestCase):
    """Test cases for profile form"""

    def test_invalid_experience_years(self):
        """Test validation of experience years"""
        from werkzeug.datastructures import MultiDict

        # Create form with MultiDict input
        form_data = MultiDict([
            ('firstname', 'John'),
            ('lastname', 'Doe'),
            ('email', 'john@example.com'),
            ('profession', 'doctor'),
            ('experience_years', '51')  # Over maximum
        ])

        form = ProfileForm(formdata=form_data)
        valid = form.validate()
        self.assertFalse(valid)
        self.assertIn('Experience years must be between 0 and 50',
                      form.experience_years.errors)
