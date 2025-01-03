#!/usr/bin/env python3
# app/routes/submission.py
"""Module for Quiz Submission routes"""
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user

from app import db
from app.models.submission import QuestionSubmission
from app.models import Question, QuestionOption, Quiz
from app.forms import QuestionSubmissionForm, ReviewSubmissionForm
from datetime import datetime

from app.utils.decorators import admin_required

submission_bp = Blueprint('submission', __name__)


@submission_bp.route('/my-submissions')
@login_required
def my_submissions():
    page = request.args.get('page', 1, type=int)
    submissions = QuestionSubmission.query.filter_by(submitter_id=current_user.id) \
        .order_by(QuestionSubmission.created_at.desc()) \
        .paginate(page=page, per_page=10)

    return render_template('submission/my_submissions.html', submissions=submissions)


@submission_bp.route('/admin/submissions')
@login_required
@admin_required
def review_submissions():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'pending')
    course = request.args.get('course')

    query = QuestionSubmission.query

    if status != 'all':
        query = query.filter_by(status=status)
    if course:
        query = query.filter_by(course=course)

    submissions = query.order_by(QuestionSubmission.created_at.asc()) \
        .paginate(page=page, per_page=20)

    return render_template('admin/submissions/review.html', submissions=submissions)


@submission_bp.route('/submit-question', methods=['GET', 'POST'])
@login_required
def submit_question():
    form = QuestionSubmissionForm()

    if form.validate_on_submit():
        # Get all options and the correct one
        options = [
            form.option1.data,
            form.option2.data,
            form.option3.data,
            form.option4.data
        ]
        correct_option_index = int(form.correct_answer.data) - 1  # Convert to 0-based index

        submission = QuestionSubmission(
            submitter_id=current_user.id,
            course=form.course.data,
            content=form.content.data,
            difficulty_level=form.difficulty_level.data,
            options=options,
            correct_option_content=options[correct_option_index],
            explanation=form.explanation.data,
            reference=form.reference.data
        )
        db.session.add(submission)
        db.session.commit()

        flash('Your question has been submitted for review. Thank you for contributing!', 'success')
        return redirect(url_for('submission.my_submissions'))

    return render_template('submission/submit.html', form=form)


@submission_bp.route('/admin/submissions/<int:submission_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def review_submission(submission_id):
    submission = QuestionSubmission.query.get_or_404(submission_id)
    form = ReviewSubmissionForm()

    if form.validate_on_submit():
        submission.status = form.status.data
        submission.feedback = form.feedback.data
        submission.reviewed_at = datetime.utcnow()
        submission.reviewed_by_id = current_user.id

        if form.status.data == 'approved':
            try:
                # Find or create question bank quiz for this course
                quiz = Quiz.query.filter_by(
                    course=submission.course,
                    is_question_bank=True
                ).first()

                if not quiz:
                    # Create new question bank quiz
                    quiz = Quiz(
                        title=f"{submission.course.replace('_', ' ').title()} Question Bank",
                        course=submission.course,
                        description="Approved community submissions",
                        is_question_bank=True,
                        created_by_id=current_user.id,
                        is_published=True,
                        passing_score=60.0,
                        time_limit=60,  # Default 60 minutes
                        profession='all',  # Question banks are available to all
                        difficulty_level='intermediate',
                        max_attempts=100,  # Unlimited attempts for question banks
                        requires_approval=False
                    )
                    db.session.add(quiz)
                    db.session.flush()

                # Create the question with a temporary correct_answer
                question = Question(
                    quiz_id=quiz.id,
                    content=submission.content,
                    question_type=submission.question_type,
                    difficulty_level=submission.difficulty_level,
                    explanation=submission.explanation,
                    created_by_id=current_user.id,
                    correct_answer=1  # Temporary value
                )
                db.session.add(question)
                db.session.flush()

                # Create options and identify the correct one
                correct_option = None
                for option_content in submission.options:
                    option = QuestionOption(
                        question_id=question.id,
                        content=option_content,
                        is_correct=(option_content == submission.correct_option_content)
                    )
                    db.session.add(option)
                    db.session.flush()

                    if option_content == submission.correct_option_content:
                        correct_option = option

                # Update question with correct option ID
                if correct_option:
                    question.correct_answer = correct_option.id
                else:
                    # Handle the case where no correct option was found
                    raise ValueError("No correct option found in submission")

                db.session.commit()
                flash('Submission approved and added to question bank.', 'success')
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f'Error approving submission: {str(e)}')
                flash('Error approving submission. Please try again.', 'error')
                return redirect(url_for('submission.review_submission', submission_id=submission_id))
        else:
            try:
                db.session.commit()
                flash(f'Submission has been {form.status.data}.', 'success')
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f'Error updating submission status: {str(e)}')
                flash('Error updating submission status. Please try again.', 'error')
                return redirect(url_for('submission.review_submission', submission_id=submission_id))

        return redirect(url_for('submission.review_submissions'))

    return render_template('admin/submissions/review_single.html',
                           submission=submission, form=form)