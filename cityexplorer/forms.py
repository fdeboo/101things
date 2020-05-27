from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, HiddenField, TextAreaField, SelectField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length, DataRequired, ValidationError, URL, Optional, Email, EqualTo
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
        user = mongo.db.users.find_one({'username': username.data})
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = mongo.db.users.find_one({'email': self.email.data})
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



class CreateLocationForm(FlaskForm):
    location = StringField('Location', validators=[InputRequired(), Length(min=2, max=25)])
    submit = SubmitField('Add Location')

    def validate_location(self, location):
        place_name = mongo.db.cities.find_one({'location': location.data})
        if place_name:
            raise ValidationError('This location has already been created.')



class CreateSuggestionForm(FlaskForm):
    location = HiddenField('Location')
    suggestion = StringField('Suggestion', validators=[InputRequired(), Length(min=2, max=50)])
    category = SelectField('Category', validators=[DataRequired()], choices=[('Museums', 'Museums'), ('Nature & Parks', 'Nature & Parks'), ('Shopping', 'Shopping'), ('Foodie Hotspots', 'Foodie Hotspots'), ('Restaurants & Bars', 'Restaurants & Bars'), ('Tourist Landmarks', 'Tourist Landmarks'), ('Theme Parks', 'Theme Parks'), ('Accommodation', 'Accommodation'), ('Theatre & Shows', 'Theatre & Shows'), ('Skyscraper', 'Skyscraper'), ('Vineyards', 'Vineyards'), ('Zoo & Aquariums', 'Zoos & Aquariums'), ('Attractions', 'Attractions'), ('PLaces of Worship', 'Places of Worship'), ('Plazas', 'Plazas'), ('Tour Groups', 'Tour Groups')])
    cost = SelectField('Cost Per Person', choices=[('Free', 'Free'), ('<10', 'Less than £10'), ('10-20', '£10-£20'), ('20-50', '£20-£50'), ('>50', 'Over £50')])
    url = StringField('Website', validators=[URL(require_tld=True), Length(min=5, max=200), Optional()])
    comment = TextAreaField('Comment', validators=[Length(min=5, max=500)])
    submit = SubmitField('Add')



class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = mongo.db.users.find_one({'email' : email.data })
        if user is None:
            raise ValidationError('There is no accaount with that email. You must register first.')
