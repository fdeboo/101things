from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length, DataRequired, ValidationError, URL, Optional
from cityexplorer import mongo


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
    cost = SelectField('Cost Per Person', choices=[('Free', 'Free'), ('Less than £10', 'Less than £10'), ('£10-20', '£10-£20'), ('£20-50', '£20-£50'), ('Over £50', 'Over £50')])
    url = StringField('Website', validators=[URL(require_tld=True), Length(min=5, max=200), Optional()])
    comment = TextAreaField('Comment', validators=[Length(min=5, max=500)])
    submit = SubmitField('Add')
