"""Base test class for all tests"""
import unittest
from app import create_app, db

"""Base test configuration and setup"""


class TestConfig:
    """Test configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # Use in-memory database
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key'
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    REDIS_URL = 'redis://localhost:6379/0'

    # Mail settings
    MAIL_SERVER = 'test-smtp.example.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'test@example.com'
    MAIL_PASSWORD = 'test-pass'
    MAIL_DEFAULT_SENDER = 'noreply@example.com'
    ADMIN_EMAIL = 'admin@example.com'

    # Add missing pagination configs
    QUIZZES_PER_PAGE = 10
    USERS_PER_PAGE = 10
    RESULTS_PER_PAGE = 10

    # Add server name for URL generation
    SERVER_NAME = 'localhost:5000'
    PREFERRED_URL_SCHEME = 'http'

    # Add upload folder configuration
    UPLOAD_FOLDER = 'tests/uploads'


class BaseTestCase(unittest.TestCase):
    """Base test case class"""

    def setUp(self):
        """Set up test environment before each test"""
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()