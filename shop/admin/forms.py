from wtforms import Form, BooleanField, StringField, PasswordField, validators, EmailField
import email_validator



class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = EmailField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password', [validators.DataRequired()])

class LoginForm(Form):
    username = StringField("Username", [validators.DataRequired()])
    password = PasswordField('New Password', [validators.DataRequired()])