"""Test cases for email functionality"""
import unittest
from unittest.mock import patch, MagicMock
from tests.test_base import BaseTestCase
from app.utils.email import (send_report_issue_notification, send_email,
                             send_password_reset_email, send_achievement_notification,
                             send_quiz_completion_email, send_welcome_email)
from app.models import User
from werkzeug.security import generate_password_hash
from app import db


class EmailTestCase(BaseTestCase):
    """Test cases for email functionality"""

    def setUp(self):
        """Set up test environment"""
        super().setUp()

        # Create test user
        self.user = User(
            first_name='Test',
            last_name='User',
            username='testuser',
            email='test@example.com',
            profession='doctor',
            password_hash=generate_password_hash('test123')
        )
        db.session.add(self.user)
        db.session.commit()

    def test_sends_report_issue_notification(self):
        """Test report issue notification email"""
        with self.app.app_context():
            with patch('app.utils.email.render_template') as mock_render:
                with patch('app.utils.email.send_email') as mock_send_email:
                    mock_render.side_effect = ['Issue report text', 'Issue report HTML']

                    issue = MagicMock()
                    issue.issue_type = 'Bug'
                    issue.screenshot_filename = 'screenshot.png'
                    issue.screenshot_data = b'screenshot data'

                    send_report_issue_notification(['admin@test.com'], issue)
                    mock_send_email.assert_called_once()
                    call_args = mock_send_email.call_args[1]
                    self.assertIn('New Issue Report', call_args['subject'])
                    self.assertEqual(['admin@test.com'], call_args['recipients'])

    def test_sends_report_issue_notification_without_screenshot(self):
        """Test report issue notification email without screenshot"""
        with self.app.app_context():
            with patch('app.utils.email.render_template') as mock_render:
                with patch('app.utils.email.send_email') as mock_send_email:
                    mock_render.side_effect = ['Issue report text', 'Issue report HTML']

                    issue = MagicMock()
                    issue.issue_type = 'Bug'
                    issue.screenshot_filename = None
                    issue.screenshot_data = None

                    send_report_issue_notification(['admin@test.com'], issue)
                    mock_send_email.assert_called_once()
                    call_args = mock_send_email.call_args[1]
                    self.assertIn('New Issue Report', call_args['subject'])
                    self.assertIsNone(call_args.get('attachments'))

    def test_sends_password_reset_email_with_invalid_token(self):
        """Test password reset email with invalid token"""
        with self.app.app_context():
            with patch('app.utils.email.render_template') as mock_render:
                with patch('app.utils.email.send_email') as mock_send_email:
                    mock_render.side_effect = ['Reset password text', 'Reset password HTML']

                    user_with_invalid_token = MagicMock()
                    user_with_invalid_token.email = 'test@example.com'
                    user_with_invalid_token.get_reset_password_token.return_value = 'invalid-token'

                    send_password_reset_email(user_with_invalid_token)
                    mock_send_email.assert_called_once()
                    call_args = mock_send_email.call_args[1]
                    self.assertIn('Reset Your Password', call_args['subject'])
                    self.assertEqual([user_with_invalid_token.email], call_args['recipients'])

    def test_sends_welcome_email_with_invalid_email(self):
        """Test welcome email with invalid email"""
        with self.app.app_context():
            with patch('app.utils.email.render_template') as mock_render:
                with patch('app.utils.email.send_email') as mock_send_email:
                    mock_render.side_effect = ['Welcome text', 'Welcome HTML']

                    invalid_user = MagicMock()
                    invalid_user.email = 'invalid-email'

                    send_welcome_email(invalid_user)
                    mock_send_email.assert_called_once()  # Still sends email even with invalid email

    def test_sends_quiz_completion_email_with_no_results(self):
        """Test quiz completion email with no results"""
        with self.app.app_context():
            with patch('app.utils.email.render_template') as mock_render:
                with patch('app.utils.email.send_email') as mock_send_email:
                    mock_render.side_effect = ['Quiz completion text', 'Quiz completion HTML']

                    quiz_result = MagicMock()
                    quiz_result.quiz = None

                    send_quiz_completion_email(self.user, quiz_result)
                    mock_send_email.assert_not_called()

    def test_sends_achievement_notification_with_empty_achievement(self):
        """Test achievement notification email with empty achievement"""
        with self.app.app_context():
            with patch('app.utils.email.render_template') as mock_render:
                with patch('app.utils.email.send_email') as mock_send_email:
                    mock_render.side_effect = ['Achievement text', 'Achievement HTML']
                    empty_achievement = {}
                    send_achievement_notification(self.user, empty_achievement)
                    mock_send_email.assert_called_once()  # Still sends email with empty achievement

    def test_sends_email_with_empty_subject(self):
        """Test sending email with empty subject"""
        with self.app.app_context():
            with patch('app.utils.email.Thread') as mock_thread:
                send_email(
                    '',
                    sender='sender@test.com',
                    recipients=['recipient@test.com'],
                    text_body='Email text body',
                    html_body='Email HTML body'
                )
                mock_thread.assert_called_once()

    def test_sends_email_with_no_recipients(self):
        """Test sending email with no recipients"""
        with self.app.app_context():
            with patch('app.utils.email.Thread') as mock_thread:
                send_email(
                    'Subject',
                    sender='sender@test.com',
                    recipients=[],
                    text_body='Email text body',
                    html_body='Email HTML body'
                )
                mock_thread.assert_not_called()

    def test_sends_email_with_invalid_attachment(self):
        """Test sending email with invalid attachment"""
        with self.app.app_context():
            with patch('app.utils.email.Thread') as mock_thread:
                send_email(
                    'Subject',
                    sender='sender@test.com',
                    recipients=['recipient@test.com'],
                    text_body='Email text body',
                    html_body='Email HTML body',
                    attachments=['nonexistent_file.txt']
                )
                mock_thread.assert_called_once()

    def test_sends_email_with_large_attachment(self):
        """Test sending email with large attachment"""
        with self.app.app_context():
            with patch('app.utils.email.Thread') as mock_thread:
                large_attachment = ('large_file.txt', b'a' * (25 * 1024 * 1024))  # 25 MB file
                send_email(
                    'Subject',
                    sender='sender@test.com',
                    recipients=['recipient@test.com'],
                    text_body='Email text body',
                    html_body='Email HTML body',
                    attachments=[large_attachment]
                )
                mock_thread.assert_called_once()


if __name__ == '__main__':
    unittest.main()