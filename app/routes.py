from flask import Flask, render_template, redirect, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from app.forms import CreateLocationForm, CreateSuggestionForm
from app import app, mongo


@app.route('/')
@app.route('/home')
def index():
    query = mongo.db.cities.find({})
    return render_template('home.html', locations=query)



@app.route('/addlocation', methods=['GET', 'POST'])
def add_location():
    form = CreateLocationForm()
    cities = mongo.db.cities
    if form.validate_on_submit():
        cities.insert(
            {
                'location':form.location.data
            }
        )
        flash("Location created", "success")
        location = form.location.data
        return redirect(url_for('add_suggestion', location=location))
    return render_template('addlocation.html', form=form)



@app.route('/addsuggestion/<location>', methods=['GET', 'POST'])
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
                    'comment' : form.comment.data
                }
            }
            })
        flash(location + " added", "success")
        return redirect(url_for('index'))
    return render_template('addsuggestion.html', location=location, form=form)


@app.route('/thingstodo/<city>', methods=['GET', 'POST'])
def suggestion_list(city):
    cities = mongo.db.cities   
    query =  cities.find_one(
        {'location': city},
        {'_id':0, 'thingsToDo':1} 
    )

    suggestions=query['thingsToDo']
    return render_template('thingstodo.html', city=city, things=suggestions, title='Things to do')