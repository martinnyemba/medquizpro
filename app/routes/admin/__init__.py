# app/routes/admin/routes.py
import os

from flask import Blueprint, render_template, request, jsonify, current_app, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.forms import QuestionForm, QuizForm
from app.models import User, Quiz, QuizResult, Question, QuestionOption
from app import db
from sqlalchemy import func, case
from datetime import datetime, timedelta, time

from app.utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    stats = {
        'total_users': User.query.count(),
        'new_users_today': User.query.filter(
            User.created_at >= datetime.utcnow().date()
        ).count(),
        'active_quizzes': Quiz.query.filter_by(is_published=True).count(),
        'quizzes_today': QuizResult.query.filter(
            QuizResult.completed_at >= datetime.utcnow().date()
        ).count(),
        'avg_score': db.session.query(func.avg(QuizResult.score)).scalar() or 0,
        'total_attempts': QuizResult.query.count(),
        'pass_rate': calculate_pass_rate()
    }

    recent_activity = get_recent_activity()
    profession_stats = get_profession_stats()

    # Chart data
    reg_dates, reg_counts = get_registration_data()
    quiz_dates, completion_counts = get_quiz_completion_data()

    return render_template('admin/dashboard.html',
                           stats=stats,
                           recent_activity=recent_activity,
                           profession_stats=profession_stats,
                           reg_dates=reg_dates,
                           reg_counts=reg_counts,
                           quiz_dates=quiz_dates,
                           completion_counts=completion_counts)


@admin_bp.route('/quiz/manage')
@login_required
@admin_required
def quiz_management():
    page = request.args.get('page', 1, type=int)
    query = Quiz.query

    # Apply filters
    course = request.args.get('course')
    status = request.args.get('status')
    profession = request.args.get('profession')
    search = request.args.get('search')

    if course:
        query = query.filter_by(course=course)
    if status:
        if status == 'published':
            query = query.filter_by(is_published=True)
        elif status == 'draft':
            query = query.filter_by(is_published=False)
    if profession:
        query = query.filter_by(profession=profession)
    if search:
        query = query.filter(Quiz.title.ilike(f'%{search}%'))

    quizzes = query.order_by(Quiz.updated_at.desc()).paginate(
        page=page, per_page=current_app.config['QUIZZES_PER_PAGE'])

    return render_template('admin/quiz/manage.html',
                           quizzes=quizzes,
                           courses=get_unique_courses(),
                           professions=get_unique_professions())


@admin_bp.route('/quiz/<int:quiz_id>/toggle-publish', methods=['POST'])
@login_required
@admin_required
def toggle_publish_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    quiz.is_published = not quiz.is_published
    db.session.commit()
    return jsonify({'success': True})


@admin_bp.route('/quiz/<int:quiz_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_quiz(quiz_id):
    """Hard delete a quiz"""
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    return jsonify({'success': True})


@admin_bp.route('/quiz/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_quiz():
    form = QuizForm()

    if form.validate_on_submit():
        quiz = Quiz(
            title=form.title.data,
            description=form.description.data,
            course=form.course.data,
            profession=form.profession.data,
            difficulty_level=form.difficulty_level.data,
            passing_score=form.passing_score.data,
            time_limit=form.time_limit.data,
            max_attempts=form.max_attempts.data,
            created_by_id=current_user.id,
            tags=form.tags.data.split(',') if form.tags.data else [],
            instructions=form.instructions.data
        )
        db.session.add(quiz)
        db.session.commit()

        flash('Quiz created successfully. Add questions now.', 'success')
        return redirect(url_for('admin.edit_questions', quiz_id=quiz.id))

    return render_template('admin/quiz/create.html', form=form)


@admin_bp.route('/quiz/<int:quiz_id>/questions', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuestionForm()

    if form.validate_on_submit():
        try:
            # First, create all options to get their IDs
            options = []
            correct_option_index = int(form.correct_answer.data)

            # Create a temporary question to associate with options
            temp_question = Question(
                quiz_id=quiz.id,
                content=form.content.data,
                question_type=form.question_type.data,
                difficulty_level=form.difficulty_level.data,
                points=form.points.data,
                explanation=form.explanation.data,
                created_by_id=current_user.id,
                correct_answer=1  # Temporary value
            )
            db.session.add(temp_question)
            db.session.flush()  # Get the question ID

            # Create options and identify the correct one
            correct_option_id = None
            for i in range(1, 5):
                # Skip creating options 3 and 4 for true/false questions
                if form.question_type.data == 'true_false' and i > 2:
                    continue

                option = QuestionOption(
                    question_id=temp_question.id,
                    content=getattr(form, f'option{i}').data,
                    is_correct=(i == correct_option_index)
                )
                db.session.add(option)
                db.session.flush()  # Get option ID

                if i == correct_option_index:
                    correct_option_id = option.id

            # Update the question with the correct option ID
            temp_question.correct_answer = correct_option_id

            # Handle image upload if provided
            if form.image.data:
                filename = secure_filename(form.image.data.filename)
                unique_filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{filename}"
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)

                # Ensure directory exists
                os.makedirs(os.path.dirname(filepath), exist_ok=True)

                # Save file
                form.image.data.save(filepath)
                temp_question.image_url = unique_filename

            # Add audit trail
            temp_question.log_change(current_user.id, {
                'action': 'create',
                'fields': {
                    'content': temp_question.content,
                    'type': temp_question.question_type,
                    'difficulty': temp_question.difficulty_level,
                    'points': temp_question.points,
                    'correct_answer': temp_question.correct_answer,
                    'options_count': len(options)
                }
            })

            db.session.commit()
            flash('Question added successfully.', 'success')
            return redirect(url_for('admin.edit_questions', quiz_id=quiz_id))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Error adding question: {str(e)}')

            # Clean up uploaded image if it exists
            if form.image.data and 'unique_filename' in locals():
                try:
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                    if os.path.exists(filepath):
                        os.remove(filepath)
                except Exception as img_e:
                    current_app.logger.error(f'Error removing uploaded image: {str(img_e)}')

            flash('An error occurred while adding the question.', 'error')
            return redirect(url_for('admin.edit_questions', quiz_id=quiz_id))

    # Get questions and prepare statistics
    questions = quiz.questions.order_by(Question.id.asc()).all()

    stats = {
        'total_questions': len(questions),
        'total_points': sum(q.points for q in questions),
        'difficulty_distribution': {
            'beginner': sum(1 for q in questions if q.difficulty_level == 'beginner'),
            'intermediate': sum(1 for q in questions if q.difficulty_level == 'intermediate'),
            'advanced': sum(1 for q in questions if q.difficulty_level == 'advanced')
        },
        'question_types': {
            'multiple_choice': sum(1 for q in questions if q.question_type == 'multiple_choice'),
            'true_false': sum(1 for q in questions if q.question_type == 'true_false')
        }
    }

    return render_template('admin/quiz/edit_questions.html',
                           quiz=quiz,
                           form=form,
                           questions=questions,
                           stats=stats)

@admin_bp.route('/question/<int:question_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id

    if question.image_url:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], question.image_url)
        if os.path.exists(filepath):
            os.remove(filepath)

    db.session.delete(question)
    db.session.commit()

    return jsonify({'success': True})


@admin_bp.route('/question/<int:question_id>', methods=['GET'])
@login_required
@admin_required
def get_question(question_id):
    """Get question data for editing"""
    question = Question.query.get_or_404(question_id)

    # Get all options and identify which one is correct based on correct_answer field
    options = question.options.all()

    # Find the index (1-based) of the correct option
    correct_option_index = None
    for index, option in enumerate(options, 1):
        if option.id == question.correct_answer:
            correct_option_index = index
            break

    return jsonify({
        'success': True,
        'question': {
            'content': question.content,
            'question_type': question.question_type,
            'difficulty_level': question.difficulty_level,
            'points': question.points,
            'explanation': question.explanation,
            'image_url': url_for('static', filename=f'uploads/{question.image_url}') if question.image_url else None,
            'options': [
                {
                    'content': option.content,
                    'is_correct': (option.id == question.correct_answer)
                } for option in options
            ],
            'correct_answer': str(correct_option_index) if correct_option_index else '1'
        }
    })


@admin_bp.route('/question/<int:question_id>/update', methods=['POST'])
@login_required
@admin_required
def update_question(question_id):
    """Update an existing Question"""
    question = Question.query.get_or_404(question_id)
    form = QuestionForm()

    if not form.validate_on_submit():
        return jsonify({
            'success': False,
            'errors': {field.name: field.errors for field in form if field.errors}
        }), 400

    try:
        # Update basic question fields
        question.content = form.content.data
        question.question_type = form.question_type.data
        question.difficulty_level = form.difficulty_level.data
        question.points = form.points.data
        question.explanation = form.explanation.data
        question.updated_by_id = current_user.id

        # Handle image update if provided
        if form.image.data:
            # Delete old image if it exists
            if question.image_url:
                old_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], question.image_url)
                if os.path.exists(old_filepath):
                    os.remove(old_filepath)

            # Save new image
            filename = secure_filename(form.image.data.filename)
            unique_filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            form.image.data.save(filepath)
            question.image_url = unique_filename

        # Get the selected correct answer index (1-based)
        correct_option_index = int(form.correct_answer.data)

        # Update existing options
        options = question.options.all()
        for i, option in enumerate(options, 1):
            option.content = getattr(form, f'option{i}').data
            # Update is_correct status
            if i == correct_option_index:
                question.correct_answer = option.id  # Update the correct_answer field

        # Log the change for audit trail
        question.log_change(current_user.id, {
            'action': 'update',
            'fields': {
                'content': question.content,
                'type': question.question_type,
                'difficulty': question.difficulty_level,
                'points': question.points,
                'explanation': question.explanation,
                'correct_answer': question.correct_answer
            }
        })

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Question updated successfully',
            'question': {
                'id': question.id,
                'content': question.content,
                'image_url': url_for('static',
                                     filename=f'uploads/{question.image_url}') if question.image_url else None,
                'difficulty_level': question.difficulty_level,
                'points': question.points,
                'options': [
                    {
                        'content': option.content,
                        'is_correct': (option.id == question.correct_answer)
                    } for option in question.options
                ],
                'explanation': question.explanation
            }
        })

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error updating question: {str(e)}')

        # Clean up uploaded image if it exists
        if form.image.data and 'unique_filename' in locals():
            try:
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
            except Exception as img_e:
                current_app.logger.error(f'Error removing uploaded image: {str(img_e)}')

        return jsonify({
            'success': False,
            'message': 'An error occurred while updating the question'
        }), 500

@admin_bp.route('/quiz/<int:quiz_id>/publish', methods=['POST'])
@login_required
@admin_required
def publish_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    if quiz.questions.count() < 1:
        return jsonify({
            'success': False,
            'message': 'Quiz must have at least one question'
        }), 400

    quiz.is_published = True
    db.session.commit()

    return jsonify({'success': True})


@admin_bp.route('/quiz/<int:quiz_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuizForm(obj=quiz)

    if form.validate_on_submit():
        form.populate_obj(quiz)
        quiz.tags = form.tags.data.split(',') if form.tags.data else []
        quiz.updated_by_id = current_user.id
        db.session.commit()
        flash('Quiz updated successfully.', 'success')
        return redirect(url_for('admin.quiz_management'))

    return render_template('admin/quiz/edit.html', form=form, quiz=quiz)


@admin_bp.route('/quiz/<int:quiz_id>/duplicate', methods=['POST'])
@login_required
@admin_required
def duplicate_quiz(quiz_id):
    original_quiz = Quiz.query.get_or_404(quiz_id)

    new_quiz = Quiz(
        title=f"Copy of {original_quiz.title}",
        description=original_quiz.description,
        course=original_quiz.course,
        profession=original_quiz.profession,
        difficulty_level=original_quiz.difficulty_level,
        passing_score=original_quiz.passing_score,
        time_limit=original_quiz.time_limit,
        max_attempts=original_quiz.max_attempts,
        created_by_id=current_user.id,
        tags=original_quiz.tags.copy() if original_quiz.tags else [],
        instructions=original_quiz.instructions,
        is_published=False
    )
    db.session.add(new_quiz)
    db.session.flush()

    for old_question in original_quiz.questions:
        new_question = Question(
            quiz_id=new_quiz.id,
            content=old_question.content,
            question_type=old_question.question_type,
            difficulty_level=old_question.difficulty_level,
            points=old_question.points,
            explanation=old_question.explanation,
            image_url=old_question.image_url
        )
        db.session.add(new_question)
        db.session.flush()

        for old_option in old_question.options:
            new_option = QuestionOption(
                question_id=new_question.id,
                content=old_option.content,
                is_correct=old_option.is_correct
            )
            db.session.add(new_option)

    db.session.commit()
    flash('Quiz duplicated successfully.', 'success')
    return redirect(url_for('admin.edit_questions', quiz_id=new_quiz.id))


@admin_bp.route('/users')
@login_required
@admin_required
def user_management():
    page = request.args.get('page', 1, type=int)
    query = User.query

    # Apply filters
    role = request.args.get('role')
    profession = request.args.get('profession')
    status = request.args.get('status')
    search = request.args.get('search')

    if role:
        query = query.filter_by(is_admin=(role == 'admin'))
    if profession:
        query = query.filter_by(profession=profession)
    if status:
        query = query.filter_by(is_active=(status == 'active'))
    if search:
        query = query.filter(
            (User.username.ilike(f'%{search}%')) |
            (User.email.ilike(f'%{search}%'))
        )

    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=current_app.config['USERS_PER_PAGE'])

    return render_template('admin/users.html', users=users)


@admin_bp.route('/settings')
@login_required
@admin_required
def settings():
    return render_template('admin/settings.html')


@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    return render_template('admin/reports.html')


# Utility functions
def calculate_pass_rate():
    total = QuizResult.query.count()
    if total == 0:
        return 0
    passed = QuizResult.query.join(Quiz).filter(
        QuizResult.score >= Quiz.passing_score
    ).count()
    return (passed / total) * 100


def get_recent_activity(limit=20):
    return QuizResult.query.join(User).order_by(
        QuizResult.completed_at.desc()
    ).limit(limit).all()


def get_profession_stats():
    stats = db.session.query(
        User.profession,
        func.count(User.id).label('users'),
        func.count(QuizResult.id).label('quizzes_taken'),
        func.coalesce(func.avg(QuizResult.score), 0).label('avg_score'),
        func.coalesce(
            func.sum(case((QuizResult.score >= Quiz.passing_score, 1), else_=0)) * 100.0 /
            func.nullif(func.count(QuizResult.id), 0),
            0
        ).label('pass_rate')
    ).outerjoin(QuizResult).outerjoin(Quiz).group_by(User.profession).all()
    return stats


def get_registration_data(days=30):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    # Cast string date to datetime.date object
    registrations = db.session.query(
        func.date(User.created_at).label('date'),
        func.count(User.id).label('count')
    ).filter(
        User.created_at >= start_date
    ).group_by('date').all()

    dates = [(start_date + timedelta(days=x)).strftime('%Y-%m-%d')
             for x in range(days)]
    counts = [0] * days

    for reg in registrations:
        reg_date = datetime.strptime(reg.date, '%Y-%m-%d').date()  # Convert string to date
        idx = (reg_date - start_date.date()).days
        if 0 <= idx < days:
            counts[idx] = reg.count

    return dates, counts


def get_quiz_completion_data(days=30):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)

    completions = db.session.query(
        func.date(QuizResult.completed_at).label('date'),
        func.count(QuizResult.id).label('count')
    ).filter(
        QuizResult.completed_at >= start_date
    ).group_by('date').all()

    dates = [(start_date + timedelta(days=x)).strftime('%Y-%m-%d')
             for x in range(days)]
    counts = [0] * days

    for comp in completions:
        idx = (datetime.strptime(comp.date, '%Y-%m-%d').date() - start_date.date()).days
        if 0 <= idx < days:
            counts[idx] = comp.count

    return dates, counts


def get_unique_courses():
    return [r[0] for r in db.session.query(Quiz.course).distinct().all()]


def get_unique_professions():
    return [r[0] for r in db.session.query(User.profession).distinct().all()]
