from flask import Flask, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from app.forms import CreateLocationForm
from app import app, mongo


@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')



@app.route('/addlocation', methods['POST'])
def add_location():
    form = CreateLocationForm()
    cities = mongo.db.cities
    if form.validate_on_submit():
        cities.insert(
            {
                'location':form.location.data,
                'picture':form.location.data
            }
        )
        location = form.location.data
        return redirect(url_for('add_activity', location=location))
    return render_template('addlocation', form=form)
