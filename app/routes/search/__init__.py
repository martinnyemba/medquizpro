# app/routes/search.py
from flask import Blueprint, render_template, request, jsonify
from app.forms import SearchForm
from app.search import search_quizzes
from app.models import Quiz, User

search_bp = Blueprint('search', __name__)


@search_bp.route('/search')
def search():
    form = SearchForm()
    # Populate dynamic choices
    form.filter_course.choices = [('', 'All Courses')] + [
        (c.course, c.course.title())
        for c in Quiz.query.with_entities(Quiz.course).distinct()
    ]
    form.filter_profession.choices = [('', 'All Professions')] + [
        (p.profession, p.profession.title())
        for p in User.query.with_entities(User.profession).distinct()
    ]

    query = request.args.get('query', '')
    filters = {
        'course': request.args.get('filter_course'),
        'profession': request.args.get('filter_profession'),
        'difficulty': request.args.get('filter_difficulty'),
        'sort_by': request.args.get('sort_by', 'newest')
    }
    page = request.args.get('page', 1, type=int)

    if query or any(filters.values()):
        results = search_quizzes(query, filters, page)
    else:
        results = None

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            'html': render_template('search/_results.html', results=results),
            'pagination': render_template('search/_pagination.html', results=results)
        })

    return render_template('search/search.html', form=form, results=results, query=query)
