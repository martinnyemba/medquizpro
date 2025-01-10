#!/usr/bin/env python3
"""Module for user authentication and authorization routes."""
import os

# app/routes/auth/auth_routes.py
from flask import Blueprint, render_template, redirect, url_for, \
    flash, request, current_app, session
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse

from werkzeug.utils import secure_filename

from app.models import User, UserAchievement, StudyGroup
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, ProfileForm
from datetime import datetime, time
import jwt
from app import db
from app.utils.email import send_email, send_welcome_email, send_password_reset_email

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()

        if user and user.check_password(form.password.data):
            if user.is_active:
                # Update user's last login info
                user.last_login = datetime.utcnow()
                user.last_ip_address = request.remote_addr

                # Store device info in the session
                session['device_info'] = {
                    'user_agent': request.user_agent.string,
                    'platform': request.user_agent.platform,
                    'browser': request.user_agent.browser
                }

                # Login the user directly
                login_user(user, remember=form.remember_me.data)

                # Commit the last login changes
                db.session.commit()

                next_page = request.args.get('next')
                if not next_page or urlparse(next_page).netloc != '':
                    next_page = url_for('main.index')

                return redirect(next_page)

            flash('Your account is deactivated. Please contact support.', 'danger')
        else:
            flash('Invalid email or password. Please check your login details', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html', title='Sign In', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.firstname.data,
            last_name=form.lastname.data,
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
    try:
        # Clear any stored session data
        session.pop('device_info', None)
        logout_user()
        flash('You have been successfully logged out.', 'success')
    except Exception as e:
        current_app.logger.error(f'Logout error: {str(e)}')
        flash('An error occurred during logout. Please try again.', 'error')

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
    """User profile route with file cleanup"""
    form = ProfileForm()

    if form.validate_on_submit():
        try:
            # Update basic profile information
            current_user.first_name = form.firstname.data
            current_user.last_name = form.lastname.data
            current_user.email = form.email.data
            current_user.profession = form.profession.data
            current_user.specialization = form.specialization.data
            current_user.experience_years = form.experience_years.data
            current_user.institution = form.institution.data
            current_user.bio = form.bio.data

            # Handle profile image if provided
            if form.profile_image.data:
                # Delete old profile image if it exists
                if current_user.profile_image:
                    # Extract filename from the path
                    old_filename = current_user.profile_image.split('/')[-1]
                    old_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], old_filename)

                    # Delete the old file if it exists
                    if os.path.exists(old_file_path):
                        try:
                            os.remove(old_file_path)
                        except OSError as e:
                            current_app.logger.error(f'Error deleting old profile image: {str(e)}')

                # Save new profile image
                filename = secure_filename(form.profile_image.data.filename)
                if filename:
                    # Generate unique filename to avoid conflicts
                    unique_filename = f"{current_user.id}_{int(time.time())}_{filename}"
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)

                    # Save the new file
                    form.profile_image.data.save(file_path)
                    current_user.profile_image = f'/uploads/{unique_filename}'

            # Handle password change if requested
            if form.new_password.data:
                if not form.current_password.data:
                    flash('Current password is required to set a new password', 'error')
                    return redirect(url_for('auth.profile'))

                if current_user.check_password(form.current_password.data):
                    current_user.password = form.new_password.data
                else:
                    flash('Current password is incorrect', 'error')
                    return redirect(url_for('auth.profile'))

            # Save changes
            db.session.commit()

            # Verify changes were saved
            db.session.refresh(current_user)
            flash('Your profile has been updated successfully.', 'success')

            return redirect(url_for('auth.profile'))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f'Profile update error: {str(e)}')
            flash('An error occurred while updating your profile. Please try again.', 'error')
            return redirect(url_for('auth.profile'))

    elif request.method == 'GET':
        # Pre-populate form fields
        form.firstname.data = current_user.first_name
        form.lastname.data = current_user.last_name
        form.email.data = current_user.email
        form.profession.data = current_user.profession
        form.specialization.data = current_user.specialization
        form.experience_years.data = current_user.experience_years
        form.institution.data = current_user.institution
        form.bio.data = current_user.bio

    # Get user's achievements and quiz statistics
    achievements = current_user.achievements.order_by(UserAchievement.earned_at.desc()).all()
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
