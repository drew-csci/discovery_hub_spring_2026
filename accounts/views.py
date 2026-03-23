from flask import render_template, redirect, url_for, request, session, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import accounts_bp
from .models import User
from .forms import UserRegistrationForm, EmailLoginForm, PasswordResetRequestForm, ResetPasswordForm
from extensions import db


@accounts_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    if current_user.is_authenticated:
        return redirect(url_for('pages.dashboard'))
    
    form = UserRegistrationForm()
    
    # Pre-select user type from query parameter or session
    user_type = request.args.get('type') or session.get('selected_user_type')
    if user_type:
        form.user_type.data = user_type
    
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.email.data,
            user_type=form.user_type.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Registration successful! Welcome to Discovery Hub.', 'success')
        
        # Redirect based on user type
        if user.user_type == 'company':
            return redirect(url_for('pages.company_dashboard'))
        return redirect(url_for('pages.screen1'))
    
    return render_template('accounts/register.html', form=form)


@accounts_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if current_user.is_authenticated:
        return redirect(url_for('pages.dashboard'))
    
    form = EmailLoginForm()
    
    # Store user type selection in session
    user_type = request.args.get('type')
    if user_type:
        session['selected_user_type'] = user_type
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'error')
            return redirect(url_for('accounts.login'))
        
        login_user(user, remember=form.remember_me.data)
        flash(f'Welcome back, {user.display_name}!', 'success')
        
        # Redirect based on user type
        if user.user_type == 'company':
            return redirect(url_for('pages.company_dashboard'))
        return redirect(url_for('pages.screen1'))
    
    return render_template('accounts/login.html', form=form, 
                         selected_user_type=session.get('selected_user_type'))


@accounts_bp.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('pages.index'))


@accounts_bp.route('/password_reset', methods=['GET', 'POST'])
def password_reset_request():
    """Request password reset"""
    if current_user.is_authenticated:
        return redirect(url_for('pages.dashboard'))
    
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # TODO: Implement email sending with token
            flash('Check your email for password reset instructions.', 'info')
        return redirect(url_for('accounts.login'))
    
    return render_template('accounts/password_reset_form.html', form=form)


@accounts_bp.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    """Reset password with token"""
    if current_user.is_authenticated:
        return redirect(url_for('pages.dashboard'))
    
    # TODO: Implement token verification
    user = None  # Verify token and get user
    
    if not user:
        flash('Invalid or expired reset link.', 'error')
        return redirect(url_for('accounts.login'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset. You can now log in.', 'success')
        return redirect(url_for('accounts.login'))
    
    return render_template('accounts/password_reset_confirm.html', form=form)
