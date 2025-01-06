#!/usr/bin/env python3
# app/routes/main.py
"""Module for main routes"""
from flask import Blueprint, render_template, current_app, flash, redirect, url_for
from flask_login import current_user

from app import db
from app.forms import ContactForm
from app.models import Quiz, User, QuizResult, UserAchievement, Question
from sqlalchemy import func
from datetime import datetime, timedelta
from sqlalchemy import desc
from app.utils.email import send_email

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    stats = {
        'total_users': User.query.count(),
        'total_quizzes': Quiz.query.filter_by(is_published=True).count(),
        'total_questions': Question.query.count(),
        'total_attempts': QuizResult.query.count()
    }

    from sqlalchemy import func, distinct
    from datetime import datetime, timedelta

    if current_user.is_authenticated:
        # Existing logic for authenticated users
        recent_quizzes = Quiz.query.filter_by(is_published=True) \
            .filter(Quiz.profession.in_(['all', current_user.profession])) \
            .order_by(Quiz.created_at.desc()).limit(6).all()

        user_stats = current_user.performance_stats
        recent_achievements = current_user.achievements \
            .filter(UserAchievement.earned_at >= datetime.utcnow() - timedelta(days=30)) \
            .order_by(UserAchievement.earned_at.desc()).limit(5).all()
    else:
        # Get distinct profession and course combinations
        prof_courses = db.session.query(
            distinct(Quiz.profession), Quiz.course
        ).filter(
            Quiz.is_published == True,
            Quiz.is_deleted == False
        ).all()

        # For each profession-course combination, get the quiz with most answered questions
        recent_quizzes = []
        for profession, course in prof_courses:
            quiz = db.session.query(
                Quiz
            ).join(
                Question, Quiz.id == Question.quiz_id
            ).filter(
                Quiz.is_published == True,
                Quiz.is_deleted == False,
                Quiz.profession == profession,
                Quiz.course == course
            ).group_by(
                Quiz.id
            ).order_by(
                func.sum(Question.times_answered).desc(),
                Quiz.created_at.desc()
            ).first()

            if quiz:  # Only add if a quiz was found
                recent_quizzes.append(quiz)

        # Limit to 6 quizzes if there are more combinations
        recent_quizzes = recent_quizzes[:6]

        user_stats = None
        recent_achievements = None

    return render_template('main/index.html',
                           stats=stats,
                           recent_quizzes=recent_quizzes,
                           user_stats=user_stats,
                           recent_achievements=recent_achievements)


@main_bp.route('/about')
def about():
    """About us page"""
    stats = {
        'total_users': User.query.count(),
        'total_quizzes': Quiz.query.filter_by(is_published=True).count(),
        'total_questions': Question.query.count(),
        'total_attempts': QuizResult.query.count()
    }
    return render_template('main/about.html', stats=stats)


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact us form page"""
    form = ContactForm()
    if form.validate_on_submit():
        # Send email to admin
        send_email(
            subject=f'Contact Form: {form.subject.data}',
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[current_app.config['ADMIN_EMAIL']],
            text_body=render_template('emails/contact_form.txt',
                                    name=form.name.data,
                                    email=form.email.data,
                                    subject=form.subject.data,
                                    message=form.message.data),
            html_body=render_template('emails/contact_form.html',
                                    name=form.name.data,
                                    email=form.email.data,
                                    subject=form.subject.data,
                                    message=form.message.data)
        )
        flash('Your message has been sent. We will get back to you soon!', 'success')
        return redirect(url_for('main.contact'))
    return render_template('main/contact.html', form=form)