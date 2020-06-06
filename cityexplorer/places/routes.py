import os
import secrets
from flask import Flask, render_template, redirect, url_for, flash, current_app, Blueprint
from flask_pymongo import PyMongo
from flask_login import current_user, login_required
from cloudinary.api import delete_resources_by_tag, resources_by_tag
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from cityexplorer.models import User
from cityexplorer.places.forms import CreateLocationForm, CreateSuggestionForm
from cityexplorer import app, mongo

places= Blueprint('places', __name__)

@places.route('/addlocation', methods=['GET', 'POST'])
@login_required
def add_location():
    form = CreateLocationForm()
    cities = mongo.db.cities
    if form.validate_on_submit():
        cities.insert(
            {
                'location':form.location.data
            }
        )
        location = form.location.data
        return redirect(url_for('places.add_suggestion', location=location))
    return render_template('addlocation.html', form=form, title="Add Location")



@places.route('/addsuggestion/<location>', methods=['GET', 'POST'])
@login_required
def add_suggestion(location):
    form = CreateSuggestionForm()
    cities = mongo.db.cities
    if form.validate_on_submit():
        cities.update(
            { 'location': location },
            { '$push': {
                'thingsToDo': {
                    'suggestion' : form.suggestion.data,
                    'category' : form.category.data,
                    'cost' : form.cost.data,
                    'url' : form.url.data,
                    'comment' : form.comment.data,
                    'author' : current_user.username
                }
            }
            })
            
        flash(location + ' added', 'success')
        return redirect(url_for('places.suggestion_list', city=location))
    return render_template('addsuggestion.html', location=location, form=form, title="Add Suggestion")



@places.route('/thingstodo/<city>', methods=['GET', 'POST'])
def suggestion_list(city):
    cities = mongo.db.cities   
    suggestions =  cities.aggregate(
        [ 
            {"$match": { "location" : city }},
            {"$unwind": "$thingsToDo"},
            {"$lookup": {
                "from": "users",
                "localField": "thingsToDo.author",
                "foreignField": "username",
                "as": "user_profile"
            }},

            {"$unwind": "$user_profile"},

            {"$project": {
                "suggestion": "$thingsToDo.suggestion",
                "cost": "$thingsToDo.cost",
                "category": "$thingsToDo.category",
                "url": "$thingsToDo.url",
                "comment": "$thingsToDo.comment",
                "author": "$user_profile.username",
                "profile": "$user_profile.picture"

                }
            }]
    )
    return render_template('thingstodo.html', city=city, things=suggestions, title='Things to do')