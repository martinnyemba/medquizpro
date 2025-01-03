# app/routes/reports.py
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from app.models import Report, Quiz, Question, User
from app.forms import ReportForm, ReportReviewForm
from app import db
from app.utils.decorators import admin_required

reports_bp = Blueprint('reports', __name__)


@reports_bp.route('/report/<item_type>/<int:item_id>', methods=['GET', 'POST'])
@login_required
def report_item(item_type, item_id):
    form = ReportForm()

    # Validate item exists
    item = None
    if item_type == 'quiz':
        item = Quiz.query.get_or_404(item_id)
    elif item_type == 'question':
        item = Question.query.get_or_404(item_id)
    elif item_type == 'user':
        item = User.query.get_or_404(item_id)

    if form.validate_on_submit():
        report = Report(
            reporter_id=current_user.id,
            reported_item_type=item_type,
            reported_item_id=item_id,
            reason=form.reason.data,
            description=form.description.data
        )
        db.session.add(report)
        db.session.commit()

        flash('Report submitted successfully.', 'success')
        return redirect(url_for('main.index'))

    return render_template('reports/report_form.html',
                           form=form, item_type=item_type, item=item)


@reports_bp.route('/admin/reports')
@login_required
@admin_required
def manage_reports():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'pending')

    query = Report.query
    if status != 'all':
        query = query.filter_by(status=status)

    reports = query.order_by(Report.created_at.desc()).paginate(
        page=page, per_page=current_app.config['ITEMS_PER_PAGE']
    )

    return render_template('admin/reports/list.html', reports=reports)



@reports_bp.route('/admin/reports/<int:report_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def review_report(report_id):
    report = Report.query.get_or_404(report_id)
    form = ReportReviewForm()

    if form.validate_on_submit():
        report.status = form.status.data
        report.resolution_notes = form.notes.data
        report.reviewed_by_id = current_user.id
        db.session.commit()

        flash('Report has been reviewed.', 'success')
        return redirect(url_for('reports.manage_reports'))

    return render_template('admin/reports/review.html', report=report, form=form)