# app/search.py
from flask import current_app
from app.models import Quiz, User, Question
from sqlalchemy import or_


def search_quizzes(query, filters=None, page=1):
    search_query = Quiz.query.filter(Quiz.is_published == True)

    if query:
        search_query = search_query.filter(
            or_(
                Quiz.title.ilike(f'%{query}%'),
                Quiz.description.ilike(f'%{query}%'),
                Quiz.tags.ilike(f'%{query}%')
            )
        )

    if filters:
        if filters.get('course'):
            search_query = search_query.filter(Quiz.course == filters['course'])
        if filters.get('profession'):
            search_query = search_query.filter(
                or_(Quiz.profession == filters['profession'], Quiz.profession == 'all')
            )
        if filters.get('difficulty'):
            search_query = search_query.filter(Quiz.difficulty_level == filters['difficulty'])

    if filters and filters.get('sort_by'):
        if filters['sort_by'] == 'newest':
            search_query = search_query.order_by(Quiz.created_at.desc())
        elif filters['sort_by'] == 'popularity':
            search_query = search_query.order_by(Quiz.total_attempts.desc())
        elif filters['sort_by'] == 'difficulty_asc':
            search_query = search_query.order_by(Quiz.difficulty_level.asc())
        elif filters['sort_by'] == 'difficulty_desc':
            search_query = search_query.order_by(Quiz.difficulty_level.desc())
    else:
        search_query = search_query.order_by(Quiz.created_at.desc())

    return search_query.paginate(
        page=page,
        per_page=current_app.config['QUIZZES_PER_PAGE'],
        error_out=False
    )