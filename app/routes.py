from flask import Flask, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from app import app, mongo


@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')