# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_caching import Cache
from flask_mail import Mail
from flask_wtf import CSRFProtect

from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os
from redis import Redis
import rq

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
migrate = Migrate()
cache = Cache()
mail = Mail()
csrf = CSRFProtect()


def create_app(config_class=Config):
    """Create and configure an instance of the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    # Redis queue
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('medical_quiz', connection=app.redis)

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.quiz import quiz_bp
    from app.routes.quiz.submission import submission_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(quiz_bp)
    app.register_blueprint(submission_bp, url_prefix='/submission')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Implement Error handlers
    from app.errors import register_error_handlers
    register_error_handlers(app)

    # Logging setup
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/medical_quiz.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Medical Quiz startup')

    # Create a Date now injector
    @app.context_processor
    def inject_now():
        """Inject current datetime into templates"""
        from datetime import datetime
        return {'now': datetime.utcnow()}

    return app
