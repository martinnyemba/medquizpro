# run.py
"""Module to run the Flask app"""
from app import create_app
from app.models import db, User, Quiz, Question, QuizResult, StudyGroup

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
