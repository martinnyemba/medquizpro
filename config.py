# config.py
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    # Basic Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secure-and-strong-hard-to-guess-string'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    # Database Configuration
    # Database configuration
    HEROKU_POSTGRESQL_WHITE_URL = os.environ.get('DATABASE_URL')
    if HEROKU_POSTGRESQL_WHITE_URL and HEROKU_POSTGRESQL_WHITE_URL.startswith("postgres://"):
        HEROKU_POSTGRESQL_WHITE_URL = HEROKU_POSTGRESQL_WHITE_URL.replace("postgres://", "postgresql+psycopg2://", 1)

    SQLALCHEMY_DATABASE_URI = HEROKU_POSTGRESQL_WHITE_URL or os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(BASEDIR, 'MedQuizPro.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis Configuration
    REDIS_URL = os.environ.get('REDISCLOUD_URL') or 'redis://localhost:6379/0'

    # Session Configuration
    SESSION_TYPE = 'redis'
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)

    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

    # Cache Configuration
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT = 300

    # Pagination
    QUIZZES_PER_PAGE = 12
    USERS_PER_PAGE = 20
    RESULTS_PER_PAGE = 15

    # Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(BASEDIR, 'app/static/uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Security Configuration
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', 'secure-salt')
    REMEMBER_COOKIE_DURATION = timedelta(days=14)
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(Config.BASEDIR, 'MedQuizPro.db')
    REMEMBER_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/medical_quiz_test'
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SSL_REDIRECT = True
    REMEMBER_COOKIE_SECURE = True

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # Production logging
        import logging
        from logging.handlers import SMTPHandler, RotatingFileHandler

        # Email error logs
        credentials = None
        if cls.MAIL_USERNAME or cls.MAIL_PASSWORD:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.MAIL_DEFAULT_SENDER,
            toaddrs=app.config['ADMINS'],
            subject='MedQuizPro Application Error',
            credentials=credentials,
            secure=() if cls.MAIL_USE_TLS else None
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

        # File logging
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler(
            'logs/medical_quiz.log',
            maxBytes=10240,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Medical Quiz startup')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
