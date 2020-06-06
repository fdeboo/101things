import os
import secrets
from flask import Flask, render_template, current_app
from flask_pymongo import PyMongo
from flask_login import current_user
from cloudinary.api import delete_resources_by_tag, resources_by_tag
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from cityexplorer.models import User
from cityexplorer import app, mongo


@app.route('/')
@app.route('/home')
def index():
    cities = mongo.db.cities
    query = cities.find({})
    if cities.find({'thingsToDo': {'$exists': False}}):
        cities.delete_many({'thingsToDo': {'$exists': False}})
        return render_template('home.html', locations=query, title="Home")
    else:
        return render_template('home.html', locations=query, title="Home")
