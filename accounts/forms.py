from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from .models import User


class UserRegistrationForm(FlaskForm):
    """User registration form"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    user_type = SelectField('Account Type', choices=[
        ('university', 'University / TTO'),
        ('company', 'Company'),
        ('investor', 'Investor')
    ], validators=[DataRequired()])
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        """Check if email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please log in or use a different email.')


class EmailLoginForm(FlaskForm):
    """Login form using email"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class PasswordResetRequestForm(FlaskForm):
    """Request password reset"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    
    def validate_email(self, email):
        """Check if email exists"""
        user = User.query.filter_by(email=email.data).first()
        if not user or not user.is_active:
            raise ValidationError('No account found with that email address.')


class ResetPasswordForm(FlaskForm):
    """Reset password form"""
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Reset Password')
