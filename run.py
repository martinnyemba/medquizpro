#!/usr/bin/env python3
# run.py
"""
Module to run the Flask app.
This file is used to run the Flask app. It creates the app and adds the models to the shell context.
"""

from app import create_app, db
from app.models import User, Quiz, Question, QuizResult, StudyGroup, UserAchievement, \
    QuestionSubmission, QuestionTag, QuestionOption, Report

# Create the Flask app instance
app = create_app()


@app.shell_context_processor
def make_shell_context():
    """
    Add models to shell context.

    This function adds the database instance and all the models to the shell context,
    allowing them to be accessed directly when using the Flask shell.

    Returns:
        dict: A dictionary containing the database instance and all the models.
    """
    return {
        'db': db,
        'User': User,
        'Quiz': Quiz,
        'Question': Question,
        'QuizResult': QuizResult,
        'StudyGroup': StudyGroup,
        'UserAchievement': UserAchievement,
        'QuestionSubmission': QuestionSubmission,
        'QuestionTag': QuestionTag,
        'QuestionOption': QuestionOption,
        'Report': Report
    }


if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
    # Run the Flask app on all available IP addresses on port 5000
    app.run(host='0.0.0.0', port=5000)
