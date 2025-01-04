# routes/auth/auth_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
from app.models import User, UserAchievement, StudyGroup
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, ProfileForm
from datetime import datetime
import jwt
from app import db
from app.utils.email import send_email

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))

        if not user.is_active:
            flash('Your account is deactivated. Please contact support.', 'error')
            return redirect(url_for('auth.login'))

        # Update last login timestamp
        user.last_login = datetime.utcnow()
        db.session.commit()

        login_user(user, remember=form.remember_me.data)

        # Handle next page redirect
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.index')

        return redirect(next_page)

    return render_template('auth/login.html', title='Sign In', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            profession=form.profession.data
        )
        user.password = form.password.data

        # Add the user to the session and flush to get the user ID
        db.session.add(user)
        db.session.flush()

        # Add welcome achievement
        achievement = UserAchievement(
            user_id=user.id,
            achievement_type='account_created',
            achievement_data={'date': datetime.utcnow().isoformat()}
        )

        # Commit both the user and achievement
        db.session.add(achievement)
        db.session.commit()

        # Send welcome email
        send_welcome_email(user)

        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout route"""
    logout_user()
    return redirect(url_for('main.index'))


@auth_bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """Request password reset route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for instructions to reset your password', 'info')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    user = User.verify_reset_password_token(token)
    if not user:
        flash('Invalid or expired reset token', 'error')
        return redirect(url_for('main.index'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form)


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile route"""
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.profession = form.profession.data
        current_user.specialization = form.specialization.data
        current_user.experience_years = form.experience_years.data
        current_user.institution = form.institution.data
        current_user.bio = form.bio.data

        if form.new_password.data:
            if current_user.check_password(form.current_password.data):
                current_user.set_password(form.new_password.data)
            else:
                flash('Current password is incorrect', 'error')
                return redirect(url_for('auth.profile'))

        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.profession.data = current_user.profession
        form.specialization.data = current_user.specialization
        form.experience_years.data = current_user.experience_years
        form.institution.data = current_user.institution
        form.bio.data = current_user.bio

    # Get user's achievements
    achievements = current_user.achievements.order_by(UserAchievement.earned_at.desc()).all()

    # Get user's quiz statistics
    quiz_stats = current_user.performance_stats

    return render_template('auth/profile.html',
                           title='Profile',
                           form=form,
                           achievements=achievements,
                           quiz_stats=quiz_stats)


@auth_bp.route('/achievements')
@login_required
def achievements():
    """User achievements route"""
    achievements = current_user.achievements.order_by(
        UserAchievement.earned_at.desc()
    ).all()

    # Group achievements by type
    achievement_groups = {}
    for achievement in achievements:
        if achievement.achievement_type not in achievement_groups:
            achievement_groups[achievement.achievement_type] = []
        achievement_groups[achievement.achievement_type].append(achievement)

    return render_template('auth/achievements.html',
                           title='My Achievements',
                           achievement_groups=achievement_groups)


@auth_bp.route('/study_groups')
@login_required
def study_groups():
    """User study groups route"""
    user_groups = current_user.study_groups
    available_groups = StudyGroup.query.filter(
        ~StudyGroup.id.in_([g.id for g in user_groups])
    ).all()

    return render_template('auth/study_groups.html',
                           title='Study Groups',
                           user_groups=user_groups,
                           available_groups=available_groups)
