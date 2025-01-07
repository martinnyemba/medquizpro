from sqlalchemy import event
from .quiz import Quiz
from .user import User, UserAchievement
from .submission import QuestionSubmission
from .question import Question, QuestionTag, QuestionOption
from .result import QuizResult
from .study_group import StudyGroup
from .report import Report
from .user_session import UserSession


# Event listeners
@event.listens_for(Quiz, 'after_update')
def update_quiz_statistics(mapper, connection, target):
    """
    Event listener for the 'after_update' event on the Quiz model.

    This function is triggered after a Quiz instance is updated.
    It calls the `update_statistics` method on the target instance to
    update the quiz statistics.

    Args:
        mapper (Mapper): The SQLAlchemy mapper.
        connection (Connection): The database connection.
        target (Quiz): The instance of the Quiz model that was updated.
    """
    target.update_statistics()


@event.listens_for(User, 'before_update')
def track_user_changes(mapper, connection, target):
    """
    Event listener for the 'before_update' event on the User model.

    This function is triggered before a User instance is updated.
    It tracks changes to the User instance's attributes and logs them
    if the `change_history` attribute is present.

    Args:
        mapper (Mapper): The SQLAlchemy mapper.
        connection (Connection): The database connection.
        target (User): The instance of the User model that is being updated.
    """
    if hasattr(target, 'change_history'):
        changes = {}
        for attr in mapper.attrs:
            hist = attr.history
            if hist.has_changes():
                changes[attr.key] = {
                    'old': hist.deleted[0] if hist.deleted else None,
                    'new': hist.added[0] if hist.added else None
                }
        if changes:
            target.log_change(target.updated_by_id, changes)