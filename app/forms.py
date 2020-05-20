from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length
from app import mongo

class CreateLocationForm(FlaskForm):
    location = StringField('Location', validators=[InputRequired(), Length(min=2, max=25))]
    submit = SubmitField('Add Location')

    def validate_location(self, location):
        place_name = mongo.db.cities.find_one({'location': location.data})
        if place_name:
            raise ValidationError('This location has already been created.')
