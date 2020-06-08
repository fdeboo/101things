from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, Email, EqualTo
from cityexplorer import mongo


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=15)])
    fname = StringField('First Name', validators=[InputRequired(), Length(min=2, max=14)])
    lname = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=14)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = mongo.db.users.find_one({'username': username.data.lower()})
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = mongo.db.users.find_one({'email': self.email.data.lower()})
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    fname = StringField('First Name', validators=[InputRequired(), Length(min=2, max=14)])
    lname = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=14)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = mongo.db.users.find_one({'email': email.data})
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
