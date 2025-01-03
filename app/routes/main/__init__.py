#!/usr/bin/env python3
# app/routes/main.py
"""Module for main routes"""
from flask import Blueprint, render_template, current_app, flash, redirect, url_for
from flask_login import current_user

from app.forms import ContactForm
from app.models import Quiz, User, QuizResult, UserAchievement
from sqlalchemy import func
from datetime import datetime, timedelta

from app.utils.email import send_email

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    stats = {
        'total_users': User.query.count(),
        'total_quizzes': Quiz.query.filter_by(is_published=True).count(),
        'total_attempts': QuizResult.query.count()
    }

    if current_user.is_authenticated:
        recent_quizzes = Quiz.query.filter_by(is_published=True) \
            .filter(Quiz.profession.in_(['all', current_user.profession])) \
            .order_by(Quiz.created_at.desc()).limit(6).all()

        user_stats = current_user.performance_stats

        # Get achievements from last 30 days
        recent_achievements = current_user.achievements \
            .filter(UserAchievement.earned_at >= datetime.utcnow() - timedelta(days=30)) \
            .order_by(UserAchievement.earned_at.desc()).limit(5).all()
    else:
        recent_quizzes = Quiz.query.filter_by(is_published=True) \
            .order_by(Quiz.created_at.desc()).limit(6).all()
        user_stats = None
        recent_achievements = None

    return render_template('main/index.html',
                           stats=stats,
                           recent_quizzes=recent_quizzes,
                           user_stats=user_stats,
                           recent_achievements=recent_achievements)


@main_bp.route('/about')
def about():
    return render_template('main/about.html')


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
            text_body=render_template('email/contact_form.txt',
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
        return redirect(url_for('static_pages.contact'))
    return render_template('main/contact.html', form=form)