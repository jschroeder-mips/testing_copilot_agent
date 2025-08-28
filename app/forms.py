"""Forms for user input validation using Flask-WTF."""

from datetime import datetime
from typing import Optional
from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    TextAreaField, 
    PasswordField, 
    SelectField, 
    DateTimeField,
    SubmitField
)
from wtforms.validators import (
    DataRequired, 
    Length, 
    Email, 
    EqualTo, 
    ValidationError,
    Optional as OptionalValidator
)
from app.models.user import User
from app.models.todo import TodoStatus, TodoPriority


class LoginForm(FlaskForm):
    """Form for user login."""
    
    username = StringField(
        'Username', 
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=80, message='Username must be between 3 and 80 characters')
        ]
    )
    password = PasswordField(
        'Password', 
        validators=[DataRequired(message='Password is required')]
    )
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """Form for user registration."""
    
    username = StringField(
        'Username', 
        validators=[
            DataRequired(message='Username is required'),
            Length(min=3, max=80, message='Username must be between 3 and 80 characters')
        ]
    )
    email = StringField(
        'Email', 
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Please enter a valid email address')
        ]
    )
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(message='Password is required'),
            Length(min=6, message='Password must be at least 6 characters long')
        ]
    )
    password2 = PasswordField(
        'Repeat Password', 
        validators=[
            DataRequired(message='Please confirm your password'),
            EqualTo('password', message='Passwords must match')
        ]
    )
    submit = SubmitField('Register')
    
    def validate_username(self, username: StringField) -> None:
        """
        Validate that username is unique.
        
        Args:
            username: Username field to validate
            
        Raises:
            ValidationError: If username already exists
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email: StringField) -> None:
        """
        Validate that email is unique.
        
        Args:
            email: Email field to validate
            
        Raises:
            ValidationError: If email already exists
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class TodoForm(FlaskForm):
    """Form for creating and editing TODO items."""
    
    title = StringField(
        'Title', 
        validators=[
            DataRequired(message='Title is required'),
            Length(min=1, max=200, message='Title must be between 1 and 200 characters')
        ]
    )
    description = TextAreaField(
        'Description',
        validators=[OptionalValidator()]
    )
    status = SelectField(
        'Status',
        choices=[
            (TodoStatus.PENDING.value, 'Pending'),
            (TodoStatus.IN_PROGRESS.value, 'In Progress'),
            (TodoStatus.COMPLETED.value, 'Completed')
        ],
        default=TodoStatus.PENDING.value
    )
    priority = SelectField(
        'Priority',
        choices=[
            (TodoPriority.LOW.value, 'Low'),
            (TodoPriority.MEDIUM.value, 'Medium'),
            (TodoPriority.HIGH.value, 'High'),
            (TodoPriority.CRITICAL.value, 'Critical')
        ],
        default=TodoPriority.MEDIUM.value
    )
    due_date = DateTimeField(
        'Due Date',
        validators=[OptionalValidator()],
        format='%Y-%m-%d %H:%M'
    )
    submit = SubmitField('Save TODO')