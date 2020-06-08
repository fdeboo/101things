from flask import render_template
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
