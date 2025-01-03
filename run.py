#!/usr/bin/env python3
# run.py
"""
Module to run the Flask app
This file is used to run the Flask app. It creates the app and adds the models to the shell context.
"""
from app import create_app, db
from app.models import User, Quiz, Question, QuizResult, StudyGroup


app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Add models to shell context"""
    return {
        'db': db,
        'User': User,
        'Quiz': Quiz,
        'Question': Question,
        'QuizResult': QuizResult,
        'StudyGroup': StudyGroup
    }


if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
