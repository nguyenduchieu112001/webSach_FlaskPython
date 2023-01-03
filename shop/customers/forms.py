from wtforms import StringField, PasswordField, SubmitField, validators, EmailField, ValidationError
import email_validator
from flask_wtf import FlaskForm

from shop.customers.models import Customer

class CustomerRegisterForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password', [validators.DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        if Customer.query.filter_by(username=username.data).first():
            raise ValidationError("This uer is already in use!")

    def validate_email(self, email):
        if Customer.query.filter_by(email=email.data).first():
            raise ValidationError("This uer is already in use!")

class CustomerLoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [validators.DataRequired()])