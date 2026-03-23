from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from . import pages_bp


@pages_bp.route('/')
def index():
    """Homepage"""
    if current_user.is_authenticated:
        return redirect(url_for('pages.dashboard'))
    return render_template('pages/index.html')


@pages_bp.route('/dashboard')
@login_required
def dashboard():
    """Main user dashboard"""
    if current_user.user_type == 'company':
        return redirect(url_for('pages.company_dashboard'))
    return render_template('pages/dashboard.html', user=current_user)


@pages_bp.route('/company_dashboard')
@login_required
def company_dashboard():
    """Company-specific dashboard"""
    if current_user.user_type != 'company':
        return redirect(url_for('pages.dashboard'))
    return render_template('pages/company_dashboard.html', user=current_user)


@pages_bp.route('/screen1')
@login_required
def screen1():
    """Onboarding screen 1"""
    return render_template('pages/screen1.html', user=current_user)
