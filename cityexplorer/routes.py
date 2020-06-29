from flask import render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user, login_required
from flask_paginate import Pagination, get_page_args
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from cityexplorer.models import User
from cityexplorer.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    RequestResetForm,
    ResetPasswordForm,
    CreateLocationForm,
    CreateSuggestionForm,
    SearchLocationForm,
)
from cityexplorer import app, mongo
from cityexplorer.utils import send_reset_email, skiplimit


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def index():
    form = SearchLocationForm()
    cities = mongo.db.cities
    searched = form.search.data
    page_num = request.args.get("page_num", default=1, type=int)
    next_num = page_num + 1
    prev_num = page_num - 1
    limit = 3
    if prev_num < 1:
        prev_num = 1
    if form.validate_on_submit():
        search = form.search.data
        results = cities.find(
            {"location": {"$regex": search, "$options": "i"}}
        )
        page_num = 1
        pages = results.count() / limit
        cur = skiplimit(page_num, results, limit)
        return render_template(
            "home.html",
            locations=cur,
            searched=searched,
            form=form,
            prev_num=prev_num,
            next_num=prev_num,
            page_num=page_num,
            pages=pages,
            title="Home",
        )
    query = cities.find({})
    if cities.find({"thingsToDo": {"$exists": False}}):
        cities.delete_many({"thingsToDo": {"$exists": False}})
    cur = skiplimit(page_num, query, limit)
    pages = query.count() / limit
    return render_template(
        "home.html",
        locations=cur,
        prev_num=prev_num,
        next_num=next_num,
        pages=pages,
        page_num=page_num,
        form=form,
        title="Home",
    )


# Users routes
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    users = mongo.db.users
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        users.insert(
            {
                "username": form.username.data.lower(),
                "fname": form.fname.data,
                "lname": form.lname.data,
                "email": form.email.data.lower(),
                "password": hashed_password,
                "picture": (
                    "https://res.cloudinary.com/fdeboo/"
                    "image/upload/v1590514314/profile_pics/default.jpg"
                ),
            }
        )
        flash("You are now registered and can log in", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form, title="Register")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({"email": form.email.data.lower()})
        if user and check_password_hash(user["password"], form.password.data):
            user_data = User(
                user["_id"],
                user["username"],
                user["fname"],
                user["lname"],
                user["email"],
            )
            login_user(user_data, remember=form.remember.data)
            next_page = request.args.get("next")
            return (
                redirect(next_page)
                if next_page
                else redirect(url_for("index"))
            )
        else:
            flash(
                "Login Unsuccessful, Please check email and password.",
                "danger",
            )
    return render_template("login.html", form=form, title="Login")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    users = mongo.db.users
    user = users.find_one({"username": current_user.username})
    if form.validate_on_submit():
        if form.picture.data:
            uploaded_image = upload(
                form.picture.data,
                folder="profile_pics",
                format="jpg",
                width=150,
                height=150,
                crop="fill",
            )
            image_url, options = cloudinary_url(uploaded_image["public_id"])
        else:
            image_url = user["picture"]
        users.update_one(
            {"username": current_user.username},
            {
                "$set": {
                    "fname": form.fname.data,
                    "lname": form.lname.data,
                    "email": form.email.data,
                    "picture": image_url,
                }
            },
        )

        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.fname.data = current_user.fname
        form.lname.data = current_user.lname
        form.email.data = current_user.email
    image_file = user["picture"]
    return render_template(
        "account.html", image_file=image_file, form=form, title="Account"
    )


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({"email": form.email.data})
        send_reset_email(user)
        flash(
            "An email has been sent with instructions to reset your password.",
            "info",
        )
        return redirect(url_for("login"))
    return render_template(
        "reset_request.html", title="Reset Password", form=form
    )


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        mongo.db.users.update_one(
            {"email": user["email"]}, {"$set": {"password": hashed_password}}
        )
        flash(
            "Your password has been updated! You are now able to log in",
            "success",
        )
        return redirect(url_for("login"))
    return render_template(
        "reset_token.html", title="Reset Password", form=form
    )


# Places routes
@app.route("/addlocation", methods=["GET", "POST"])
@login_required
def add_location():
    form = CreateLocationForm()
    cities = mongo.db.cities
    if form.validate_on_submit():
        cities.insert({"location": form.location.data})
        location = form.location.data
        return redirect(url_for("add_suggestion", location=location))
    return render_template("addlocation.html", form=form, title="Add Location")


@app.route("/addsuggestion/<location>", methods=["GET", "POST"])
@login_required
def add_suggestion(location):
    form = CreateSuggestionForm()
    cities = mongo.db.cities
    if form.validate_on_submit():
        cities.update(
            {"location": location},
            {
                "$push": {
                    "thingsToDo": {
                        "suggestion": form.suggestion.data,
                        "category": form.category.data,
                        "cost": form.cost.data,
                        "url": form.url.data,
                        "comment": form.comment.data,
                        "author": current_user.username,
                    }
                }
            },
        )

        flash(location + " added", "success")
        return redirect(url_for("suggestion_list", city=location))
    return render_template(
        "addsuggestion.html",
        location=location,
        form=form,
        title="Add Suggestion",
    )


@app.route("/thingstodo/<city>", methods=["GET", "POST"])
def suggestion_list(city):
    cities = mongo.db.cities
    page, per_page, offset = get_page_args(
        page_parameter="page", per_page_parameter="per_page"
    )
    per_page = 3
    offset = page * per_page
    page = request.args.get("page", type=int, default=1)
    suggestions = cities.aggregate(
        [
            {"$match": {"location": city}},
            {"$unwind": "$thingsToDo"},
            {
                "$lookup": {
                    "from": "users",
                    "localField": "thingsToDo.author",
                    "foreignField": "username",
                    "as": "user_profile",
                }
            },
            {"$unwind": "$user_profile"},
            {
                "$project": {
                    "suggestion": "$thingsToDo.suggestion",
                    "cost": "$thingsToDo.cost",
                    "category": "$thingsToDo.category",
                    "url": "$thingsToDo.url",
                    "comment": "$thingsToDo.comment",
                    "author": "$user_profile.username",
                    "profile": "$user_profile.picture",
                }
            },
        ]
    )

    array = list(suggestions)
    total = len(array)
    posts = array[offset: offset + per_page]
    pagination = Pagination(
        page=page, per_page=per_page, total=total, css_framework="bootstrap4"
    )
    return render_template(
        "thingstodo.html",
        city=city,
        things=posts,
        page=page,
        per_page=per_page,
        pagination=pagination,
        title="Things to do",
    )
