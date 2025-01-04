from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib
import os
from threading import Thread
from flask import current_app, render_template
from app import create_app


def send_async_email(app, msg, smtp_settings):
    with app.app_context():
        with smtplib.SMTP(smtp_settings['server'], smtp_settings['port']) as server:
            if smtp_settings['use_tls']:
                server.starttls()
            if smtp_settings['username'] and smtp_settings['password']:
                server.login(smtp_settings['username'], smtp_settings['password'])
            server.send_message(msg)


def send_email(subject, sender, recipients, text_body, html_body, attachments=None):
    app = current_app._get_current_object()
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    # Add text and HTML parts
    part1 = MIMEText(text_body, 'plain')
    part2 = MIMEText(html_body, 'html')
    msg.attach(part1)
    msg.attach(part2)

    # Add attachments if any
    if attachments:
        for attachment in attachments:
            if isinstance(attachment, str) and os.path.isfile(attachment):
                with open(attachment, 'rb') as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(attachment))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                msg.attach(part)
            elif isinstance(attachment, tuple):
                filename, data = attachment
                part = MIMEApplication(data, Name=filename)
                part['Content-Disposition'] = f'attachment; filename="{filename}"'
                msg.attach(part)

    smtp_settings = {
        'server': app.config['MAIL_SERVER'],
        'port': app.config['MAIL_PORT'],
        'use_ssl': app.config['MAIL_USE_SSL'],
        'username': app.config['MAIL_USERNAME'],
        'password': app.config['MAIL_PASSWORD']
    }

    Thread(target=send_async_email, args=(app, msg, smtp_settings)).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email(
        '[Medical Quiz] Reset Your Password',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email],
        text_body=render_template('emails/reset_password.txt',
                                  user=user, token=token),
        html_body=render_template('emails/reset_password.html',
                                  user=user, token=token)
    )


def send_welcome_email(user):
    send_email(
        '[Medical Quiz] Welcome to Medical Quiz',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email],
        text_body=render_template('emails/welcome.txt', user=user),
        html_body=render_template('emails/welcome.html', user=user)
    )


def send_quiz_completion_email(user, quiz_result):
    send_email(
        f'[Medical Quiz] {quiz_result.quiz.title} - Results',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email],
        text_body=render_template('emails/quiz_completion.txt',
                                  user=user, result=quiz_result),
        html_body=render_template('emails/quiz_completion.html',
                                  user=user, result=quiz_result)
    )


def send_achievement_notification(user, achievement):
    send_email(
        '[Medical Quiz] New Achievement Unlocked!',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=[user.email],
        text_body=render_template('emails/achievement.txt',
                                  user=user, achievement=achievement),
        html_body=render_template('emails/achievement.html',
                                  user=user, achievement=achievement)
    )


def send_report_issue_notification(admin_emails, issue):
    send_email(
        f'[Medical Quiz] New Issue Report: {issue.issue_type}',
        sender=current_app.config['MAIL_DEFAULT_SENDER'],
        recipients=admin_emails,
        text_body=render_template('emails/issue_report.txt', issue=issue),
        html_body=render_template('emails/issue_report.html', issue=issue),
        attachments=[(issue.screenshot_filename, issue.screenshot_data)] if issue.screenshot_data else None
    )
