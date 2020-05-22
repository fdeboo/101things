from flask import Flask, render_template, redirect, url_for, flash, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from cityexplorer.models import User
from cityexplorer.forms import CreateLocationForm, CreateSuggestionForm, RegistrationForm, LoginForm, UpdateAccountForm
from cityexplorer import app, mongo


@app.route('/')
@app.route('/home')
def index():
    query = mongo.db.cities.find({})
    return render_template('home.html', locations=query, title="Home")



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
    return render_template('addlocation.html', form=form, title="Add Location")



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
            
        flash(location + 'added', 'success')
        return redirect(url_for('index'))
    return render_template('addsuggestion.html', location=location, form=form, title="Add Suggestion")



@app.route('/thingstodo/<city>', methods=['GET', 'POST'])
def suggestion_list(city):
    cities = mongo.db.cities   
    query =  cities.find_one(
        {'location': city},
        {'_id':0, 'thingsToDo':1} 
    )
    suggestions=query['thingsToDo']
    return render_template('thingstodo.html', city=city, things=suggestions, title='Things to do')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    users = mongo.db.users
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        users.insert({'username': form.username.data, 'fname': form.fname.data, 'lname': form.lname.data, 'email': form.email.data, 'password': hashed_password, 'picture' : "default.jpg"})
        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title="Register")



@app.route('/login', methods= ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({'email': form.email.data})
        if user and check_password_hash(user['password'], form.password.data):
            user_data = User(user['_id'], user['username'], user['email'])
            login_user(user_data, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful, Please check email and password.', 'danger')
    return render_template('login.html', form=form, title="Login")



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    users = mongo.db.users

    if form.validate_on_submit():
        users.update_one({'username' : current_user.username }, { '$set' : {'username' : form.username.data, 'email' : form.email.data}})
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.fname.data = current_user.fname
        form.lname.data = current_user.lname
        form.email.data = current_user.email
    return render_template('account.html', form=form, title='Account')
