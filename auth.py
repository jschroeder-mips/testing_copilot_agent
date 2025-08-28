"""Authentication blueprint for user registration and login."""
from typing import Optional
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import db, User

auth = Blueprint('auth', __name__)


class LoginForm(FlaskForm):
    """Form for user login."""
    
    username = StringField(
        'Username', 
        validators=[DataRequired(), Length(min=3, max=80)],
        render_kw={'class': 'input is-dark', 'placeholder': 'Enter your username'}
    )
    password = PasswordField(
        'Password', 
        validators=[DataRequired()],
        render_kw={'class': 'input is-dark', 'placeholder': 'Enter your password'}
    )
    submit = SubmitField(
        'LOGIN', 
        render_kw={'class': 'button is-primary is-fullwidth'}
    )


class RegistrationForm(FlaskForm):
    """Form for user registration."""
    
    username = StringField(
        'Username', 
        validators=[DataRequired(), Length(min=3, max=80)],
        render_kw={'class': 'input is-dark', 'placeholder': 'Choose a username'}
    )
    email = EmailField(
        'Email', 
        validators=[DataRequired(), Email()],
        render_kw={'class': 'input is-dark', 'placeholder': 'Enter your email'}
    )
    password = PasswordField(
        'Password', 
        validators=[DataRequired(), Length(min=6)],
        render_kw={'class': 'input is-dark', 'placeholder': 'Create a password'}
    )
    password2 = PasswordField(
        'Confirm Password', 
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')],
        render_kw={'class': 'input is-dark', 'placeholder': 'Confirm your password'}
    )
    submit = SubmitField(
        'REGISTER', 
        render_kw={'class': 'button is-primary is-fullwidth'}
    )
    
    def validate_username(self, username: StringField) -> None:
        """Validate that username is unique."""
        user: Optional[User] = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email: EmailField) -> None:
        """Validate that email is unique."""
        user: Optional[User] = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')


@auth.route('/login', methods=['GET', 'POST'])
def login() -> str:
    """Handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user: Optional[User] = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        
        flash('Invalid username or password', 'error')
    
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register() -> str:
    """Handle user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        
        try:
            db.session.add(user)
            db.session.commit()
            flash(f'Registration successful! Welcome, {user.username}!', 'success')
            login_user(user, remember=True)
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('register.html', form=form)


@auth.route('/logout')
@login_required
def logout() -> str:
    """Handle user logout."""
    username = current_user.username
    logout_user()
    flash(f'Goodbye, {username}!', 'info')
    return redirect(url_for('auth.login'))