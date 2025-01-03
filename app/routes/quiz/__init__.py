# routes/quiz/quiz_routes.py
from flask import Blueprint, render_template, request, jsonify, current_app, abort, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import Forbidden, BadRequest

from app import db
from app.models import Quiz, Question, QuizResult, User, UserAchievement
from app.utils.decorators import profession_required
from sqlalchemy import func
from datetime import datetime
import json

quiz_bp = Blueprint('quiz', __name__)


def get_filtered_quizzes(page, per_page, filters):
    """Helper function to get filtered quizzes"""
    query = Quiz.query.filter_by(is_deleted=False, is_published=True)

    if filters.get('course'):
        query = query.filter_by(course=filters['course'])
    if filters.get('difficulty'):
        query = query.filter_by(difficulty_level=filters['difficulty'])
    if filters.get('profession') != 'all':
        query = query.filter(Quiz.profession.in_(['all', filters['profession']]))

    return query.order_by(Quiz.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)


@quiz_bp.route('/quizzes')
@login_required
def list_quizzes():
    """List available quizzes with filtering and pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = current_app.config.get('QUIZZES_PER_PAGE', 10)

        filters = {
            'course': request.args.get('course'),
            'difficulty': request.args.get('difficulty'),
            'profession': request.args.get('profession', current_user.profession)
        }

        quizzes = get_filtered_quizzes(page, per_page, filters)

        # Get filter options
        courses = db.session.query(Quiz.course).distinct().all()
        difficulty_levels = db.session.query(Quiz.difficulty_level).distinct().all()

        return render_template('quiz/list.html',
                               quizzes=quizzes,
                               courses=[course[0] for course in courses],
                               difficulty_levels=[level[0] for level in difficulty_levels],
                               current_filters=filters)
    except Exception as e:
        current_app.logger.error(f"Error in list_quizzes: {str(e)}")
        flash('An error occurred while loading quizzes.', 'error')
        return redirect(url_for('main.index'))


@quiz_bp.route('/quiz/<int:quiz_id>')
@login_required
def take_quiz(quiz_id):
    """Start or resume a quiz"""
    try:
        quiz = Quiz.query.filter_by(id=quiz_id, is_deleted=False).first_or_404()

        # Check profession requirements
        if quiz.profession != 'all' and quiz.profession != current_user.profession:
            raise Forbidden("You don't have permission to take this quiz.")

        # Check attempt limits
        attempt_count = QuizResult.query.filter_by(
            user_id=current_user.id,
            quiz_id=quiz_id,
            is_deleted=False
        ).count()

        if attempt_count >= quiz.max_attempts:
            flash('Maximum attempts reached for this quiz.', 'error')
            return redirect(url_for('quiz.list_quizzes'))

        # Check for in-progress attempt
        existing_attempt = QuizResult.query.filter_by(
            user_id=current_user.id,
            quiz_id=quiz_id,
            status='in_progress',
            is_deleted=False
        ).first()

        if existing_attempt:
            return redirect(url_for('quiz.resume_quiz', result_id=existing_attempt.id))

        # Create new attempt
        questions = quiz.questions.filter_by(is_deleted=False).all()
        if not questions:
            flash('This quiz has no questions available.', 'error')
            return redirect(url_for('quiz.list_quizzes'))

        quiz_result = QuizResult(
            user_id=current_user.id,
            quiz_id=quiz_id,
            attempt_number=attempt_count + 1,
            answers=[],
            status='in_progress'
        )
        db.session.add(quiz_result)
        db.session.commit()

        return render_template('quiz/take_quiz.html',
                               quiz=quiz,
                               questions=questions,
                               quiz_result=quiz_result)

    except Forbidden as e:
        flash(str(e), 'error')
        return redirect(url_for('quiz.list_quizzes'))
    except Exception as e:
        current_app.logger.error(f"Error in take_quiz: {str(e)}")
        flash('An error occurred while loading the quiz.', 'error')
        return redirect(url_for('quiz.list_quizzes'))


@quiz_bp.route('/quiz/submit/<int:result_id>', methods=['POST'])
@login_required
def submit_quiz(result_id):
    try:
        quiz_result = QuizResult.query.get_or_404(result_id)

        if quiz_result.user_id != current_user.id:
            raise Forbidden("You don't have permission to submit this quiz.")

        if quiz_result.status == 'completed':
            raise BadRequest('This quiz has already been submitted.')

        data = request.get_json()
        if not data or 'answers' not in data:
            raise BadRequest('Invalid submission data.')

        # Format and validate answers
        formatted_answers = []
        total_points = 0
        earned_points = 0

        for question_id, answer_id in data['answers'].items():
            question = Question.query.get(int(question_id))
            if not question:
                continue

            is_correct = question.check_answer(answer_id)
            total_points += question.points
            if is_correct:
                earned_points += question.points

            formatted_answers.append({
                'question_id': int(question_id),
                'answer': int(answer_id),
                'is_correct': is_correct
            })

        quiz_result.answers = formatted_answers
        quiz_result.completed_at = datetime.utcnow()
        quiz_result.time_taken = data.get('time_taken', 0)
        quiz_result.status = 'completed'
        quiz_result.score = (earned_points / total_points * 100) if total_points > 0 else 0

        if quiz_result.score >= quiz_result.quiz.passing_score:
            achievement = UserAchievement(
                user_id=current_user.id,
                achievement_type='quiz_passed',
                achievement_data={
                    'quiz_id': quiz_result.quiz_id,
                    'score': quiz_result.score,
                    'passing_score': quiz_result.quiz.passing_score
                }
            )
            db.session.add(achievement)

        db.session.commit()

        return jsonify({
            'success': True,
            'score': quiz_result.score,
            'redirect_url': url_for('quiz.view_result', result_id=result_id)
        })

    except (Forbidden, BadRequest) as e:
        return jsonify({'success': False, 'error': str(e)}), e.code
    except Exception as e:
        current_app.logger.error(f"Error in submit_quiz: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'error': 'An error occurred while submitting the quiz.'}), 500


@quiz_bp.route('/quiz/resume/<int:result_id>')
@login_required
def resume_quiz(result_id):
    """Resume an incomplete quiz attempt"""
    quiz_result = QuizResult.query.get_or_404(result_id)

    # Verify ownership
    if quiz_result.user_id != current_user.id:
        abort(403)

    # Get quiz details
    quiz = quiz_result.quiz
    questions = quiz.questions.filter_by(is_deleted=False).all()

    return render_template('quiz/take_quiz.html',
                           quiz=quiz,
                           questions=questions,
                           quiz_result=quiz_result)


@quiz_bp.route('/quiz/result/<int:result_id>')
@login_required
def view_result(result_id):
    """View quiz results with detailed feedback and analytics"""
    try:
        result = QuizResult.query.filter_by(id=result_id, is_deleted=False).first_or_404()

        # Verify ownership or admin status
        if result.user_id != current_user.id and not current_user.is_admin:
            raise Forbidden("You don't have permission to view these results.")

        # Ensure quiz is completed
        if result.status != 'completed':
            flash('This quiz attempt has not been completed yet.', 'warning')
            return redirect(url_for('quiz.resume_quiz', result_id=result_id))

        # Get question details and process answers
        questions = {q.id: q for q in result.quiz.questions.filter_by(is_deleted=False).all()}
        processed_answers = []
        total_points = 0
        earned_points = 0

        for answer in result.answers:
            question = questions.get(answer['question_id'])
            if question:
                # Get user's selected option
                user_option = next((opt for opt in question.options
                                    if str(opt.id) == str(answer['answer'])), None)

                # Get correct option
                correct_option = next((opt for opt in question.options
                                       if str(opt.id) == str(question.correct_answer)), None)

                is_correct = str(answer['answer']) == str(question.correct_answer)
                total_points += question.points
                if is_correct:
                    earned_points += question.points

                processed_answers.append({
                    'question': question,
                    'user_answer': user_option,
                    'correct_answer': correct_option,
                    'is_correct': is_correct,
                    'points': question.points,
                    'explanation': question.explanation
                })

        # Calculate statistics
        stats = {
            'total_questions': len(processed_answers),
            'correct_answers': sum(1 for a in processed_answers if a['is_correct']),
            'total_points': total_points,
            'earned_points': earned_points,
            'accuracy': (earned_points / total_points * 100) if total_points > 0 else 0,
            'time_taken': result.time_taken or 0,
            'completion_time': result.completed_at.strftime('%Y-%m-%d %H:%M:%S') if result.completed_at else None
        }

        # Get user's performance history
        user_history = QuizResult.query.filter_by(
            user_id=current_user.id,
            quiz_id=result.quiz_id,
            status='completed',
            is_deleted=False
        ).order_by(QuizResult.created_at.desc()).limit(5).all()

        return render_template('quiz/result.html',
                               result=result,
                               answers=processed_answers,
                               quiz=result.quiz,
                               stats=stats,
                               user_history=user_history)

    except Forbidden as e:
        flash(str(e), 'error')
        return redirect(url_for('quiz.list_quizzes'))
    except Exception as e:
        current_app.logger.error(f"Error in view_result: {str(e)}")
        flash('An error occurred while loading the results.', 'error')
        return redirect(url_for('quiz.list_quizzes'))


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
