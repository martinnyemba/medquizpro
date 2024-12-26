# routes/quiz/quiz_routes.py
from flask import Blueprint, render_template, request, jsonify, current_app, abort, flash, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.models import Quiz, Question, QuizResult, User, UserAchievement
from app.utils.decorators import profession_required
from sqlalchemy import func
from datetime import datetime
import json

quiz_bp = Blueprint('quiz', __name__)


@quiz_bp.route('/quizzes')
@login_required
def list_quizzes():
    """List available quizzes with filtering and pagination"""
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['QUIZZES_PER_PAGE']

    # Filter parameters
    course = request.args.get('course')
    difficulty = request.args.get('difficulty')
    profession = request.args.get('profession', current_user.profession)

    # Base query
    query = Quiz.query.filter_by(is_deleted=False, is_published=True)

    # Apply filters
    if course:
        query = query.filter_by(course=course)
    if difficulty:
        query = query.filter_by(difficulty_level=difficulty)
    if profession != 'all':
        query = query.filter(Quiz.profession.in_(['all', profession]))

    # Get paginated results
    quizzes = query.order_by(Quiz.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)

    # Get available courses and difficulty levels for filters
    courses = db.session.query(Quiz.course).distinct().all()
    difficulty_levels = db.session.query(Quiz.difficulty_level).distinct().all()

    return render_template('quiz/list.html',
                           quizzes=quizzes,
                           courses=courses,
                           difficulty_levels=difficulty_levels,
                           current_filters={
                               'course': course,
                               'difficulty': difficulty,
                               'profession': profession
                           })


@quiz_bp.route('/quiz/<int:quiz_id>')
@login_required
def take_quiz(quiz_id):
    """Start or resume a quiz"""
    quiz = Quiz.query.get_or_404(quiz_id)

    # Check profession requirements
    if quiz.profession != 'all' and quiz.profession != current_user.profession:
        abort(403)

    # Check if user has exceeded maximum attempts
    attempt_count = QuizResult.query.filter_by(
        user_id=current_user.id,
        quiz_id=quiz_id,
        is_deleted=False
    ).count()

    if attempt_count >= quiz.max_attempts:
        flash('You have exceeded the maximum number of attempts for this quiz.', 'error')
        return redirect(url_for('quiz.list_quizzes'))

    # Check for existing incomplete attempt
    existing_attempt = QuizResult.query.filter_by(
        user_id=current_user.id,
        quiz_id=quiz_id,
        status='in_progress',
        is_deleted=False
    ).first()

    if existing_attempt:
        return redirect(url_for('quiz.resume_quiz', result_id=existing_attempt.id))

    # Create new quiz attempt
    questions = quiz.questions.filter_by(is_deleted=False).all()
    quiz_result = QuizResult(
        user_id=current_user.id,
        quiz_id=quiz_id,
        attempt_number=attempt_count + 1,
        answers={},
        status='in_progress'
    )
    db.session.add(quiz_result)
    db.session.commit()

    return render_template('quiz/take_quiz.html',
                           quiz=quiz,
                           questions=questions,
                           quiz_result=quiz_result)


@quiz_bp.route('/quiz/submit/<int:result_id>', methods=['POST'])
@login_required
def submit_quiz(result_id):
    """Submit quiz answers and calculate results"""
    quiz_result = QuizResult.query.get_or_404(result_id)

    # Verify ownership
    if quiz_result.user_id != current_user.id:
        abort(403)

    # Get answers from request
    answers = request.get_json()

    # Update quiz result
    quiz_result.answers = answers
    quiz_result.completed_at = datetime.utcnow()
    quiz_result.status = 'completed'
    quiz_result.calculate_score()

    # Update user achievements
    if quiz_result.score >= quiz_result.quiz.passing_score:
        achievement = UserAchievement(
            user_id=current_user.id,
            achievement_type='quiz_passed',
            achievement_data={
                'quiz_id': quiz_result.quiz_id,
                'score': quiz_result.score
            }
        )
        db.session.add(achievement)

    db.session.commit()

    return jsonify({
        'success': True,
        'redirect_url': url_for('quiz.view_result', result_id=result_id)
    })


@quiz_bp.route('/quiz/result/<int:result_id>')
@login_required
def view_result(result_id):
    """View quiz results with detailed feedback"""
    result = QuizResult.query.get_or_404(result_id)

    # Verify ownership or admin status
    if result.user_id != current_user.id and not current_user.is_admin:
        abort(403)

    # Get question details for answers
    questions = {q.id: q for q in result.quiz.questions.all()}

    # Process answers for display
    processed_answers = []
    for answer in result.answers:
        question = questions.get(answer['question_id'])
        if question:
            processed_answers.append({
                'question': question,
                'user_answer': answer['answer'],
                'is_correct': answer['answer'] == question.correct_answer,
                'explanation': question.explanation
            })

    return render_template('quiz/result.html',
                           result=result,
                           answers=processed_answers,
                           quiz=result.quiz)


@quiz_bp.route('/quiz/analytics/<int:quiz_id>')
@login_required
def quiz_analytics(quiz_id):
    """View detailed quiz analytics"""
    quiz = Quiz.query.get_or_404(quiz_id)

    # Get general statistics
    total_attempts = QuizResult.query.filter_by(quiz_id=quiz_id).count()
    avg_score = db.session.query(func.avg(QuizResult.score)) \
                    .filter_by(quiz_id=quiz_id).scalar() or 0

    # Get question statistics
    question_stats = []
    for question in quiz.questions:
        if question.times_answered > 0:
            success_rate = (question.times_correct / question.times_answered) * 100
        else:
            success_rate = 0
        question_stats.append({
            'question': question.content,
            'success_rate': success_rate,
            'times_answered': question.times_answered
        })

    # Get profession breakdown
    profession_stats = db.session.query(
        User.profession,
        func.count(QuizResult.id).label('attempts'),
        func.avg(QuizResult.score).label('avg_score')
    ).join(QuizResult).filter(QuizResult.quiz_id == quiz_id) \
        .group_by(User.profession).all()

    return render_template('quiz/analytics.html',
                           quiz=quiz,
                           total_attempts=total_attempts,
                           avg_score=avg_score,
                           question_stats=question_stats,
                           profession_stats=profession_stats)