""" Imports include json to convert a python list to json array,   """
import json
from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    g,
)
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
    UpdateSuggestionForm,
    SearchLocationForm,
    FilterResultsForm,
)
from cityexplorer import app, mongo
from cityexplorer.utils import send_reset_email


@app.context_processor
def context_processor():
    """ Function can be called from any template in the app.
    Processes the logic required to return a value to the template.
    In this case, queries the database for all suggestions and their authors.
    Returns the results to the template as a list, with the key name
    'suggestions' """

    query = mongo.db.cities.aggregate(
        [
            {"$unwind": "$thingsToDo"},
            {
                "$project": {
                    "author": "$thingsToDo.author",
                    "suggestion": "$thingsToDo.suggestion",
                }
            },
        ]
    )
    return dict(suggestions=list(query))


@app.before_request
def before_request_func():
    """ Instantiates the SearchLocationForm so that it can be
    accessed globally in the app """

    g.searchform = SearchLocationForm()


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def index():
    """ If a search term is submitted, queries the database for case-
    insensitive matches. Otherwise, queries the database for all documents.

    Passes the results to the template in a limited batch so that large numbers
    of results are divided over several pages and are paginated.
    Displays results for all locations in the database """

    cities = mongo.db.cities
    searched = ""
    page, per_page, offset = get_page_args(
        page_parameter="page", per_page_parameter="per_page"
    )
    per_page = 4
    offset = (page - 1) * per_page
    if g.searchform.validate_on_submit():
        searched = g.searchform.q.data
        query = cities.find(
            {"location": {"$regex": searched, "$options": "i"}}
        )
    else:
        query = cities.find({})
        if cities.find({"thingsToDo": {"$exists": False}}):
            cities.delete_many({"thingsToDo": {"$exists": False}})
    total = query.count()
    locations = query[offset: offset + per_page]
    pagination = Pagination(
        page=page, per_page=per_page, total=total, css_framework="bootstrap4"
    )
    return render_template(
        "home.html",
        locations=locations,
        searched=searched,
        page=page,
        per_page=per_page,
        pagination=pagination,
        title="Home",
    )


# Users routes
@app.route("/register", methods=["GET", "POST"])
def register():
    """ Description """
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
    """ Description """
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
    """ Logs the user out using logout_user function from flask_login and
    redirects them to the home page """

    logout_user()
    return redirect(url_for("index"))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """ Description """
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
            image_url = cloudinary_url(uploaded_image["public_id"])
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
    cities = mongo.db.cities
    query = ""
    page, per_page, offset = get_page_args(
        page_parameter="page", per_page_parameter="per_page"
    )
    query = cities.aggregate(
        [
            {"$unwind": "$thingsToDo"},
            {"$match": {"thingsToDo.author": current_user.username}},
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
    results = list(query)

    total = len(results)
    per_page = 10
    offset = (page - 1) * per_page
    suggestions = results[offset: offset + per_page]
    pagination = Pagination(
        page=page, per_page=per_page, total=total, css_framework="bootstrap4"
    )
    print(str(suggestions))
    return render_template(
        "account.html",
        image_file=image_file,
        things=suggestions,
        page=page,
        per_page=per_page,
        pagination=pagination,
        form=form,
        title="Account",
    )


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    """ Description """
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
    """ Description """
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
    """ Instantiates the Location form. Inserts a new document using data
    retrieved from the form input """

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
    """ Instanstiates the suggestion form. Updates the database using the
    data retrieved from the form input. Redirects to the thingsToDo template.
    """

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


@app.route("/thingstodo/<city>", methods=["GET"])
def suggestion_list(city):
    """ Runs a search for all documents in the database. If there is a filter
    applied in the FilterResultsForm, uses the data retrieved from the page
    arguements to construct the criteria for the match pipeline, used in a
    mongo aggregation query. 
    
    Converts the results of the query to a list type.
    The number of list items returned to the template is limited to a batch of
    10. Pagination using flask_paginate handles the page number and offset
    for paging through to further batches of results. """

    form = FilterResultsForm()
    edit_form = UpdateSuggestionForm()
    cities = mongo.db.cities
    location = cities.find_one(
        {"location": city}, {"_id": 0, "location": 1, "bg_img": 1}
    )
    query = ""
    filters = []
    page, per_page, offset = get_page_args(
        page_parameter="page", per_page_parameter="per_page"
    )

    if request.args.get("category") or request.args.get("cost"):
        condition_a = []
        condition_b = []
        if request.args.get("category"):
            cat_filters = request.args.getlist("category")
            for category in cat_filters:
                cat_dict = {}
                cat_dict["thingsToDo.category"] = category
                condition_a.append(cat_dict)
                filters.append(category)
        if request.args.get("cost"):
            cost_filters = request.args.getlist("cost")
            for cost in cost_filters:
                cost_dict = {}
                cost_dict["thingsToDo.cost"] = cost
                condition_b.append(cost_dict)
                filters.append(cost)
        if len(condition_b) == 0:
            query = cities.aggregate(
                [
                    {"$unwind": "$thingsToDo"},
                    {"$match": {"location": city, "$or": condition_a}},
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
        elif len(condition_a) == 0:
            query = cities.aggregate(
                [
                    {"$unwind": "$thingsToDo"},
                    {"$match": {"location": city, "$or": condition_b}},
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

        else:
            query = cities.aggregate(
                [
                    {"$unwind": "$thingsToDo"},
                    {
                        "$match": {
                            "location": city,
                            "$and": [
                                {"$or": condition_a},
                                {"$or": condition_b},
                            ],
                        }
                    },
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

    else:
        query = cities.aggregate(
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
    results = list(query)
    total = len(results)
    per_page = 10
    offset = (page - 1) * per_page
    suggestions = results[offset: offset + per_page]
    pagination = Pagination(
        page=page, per_page=per_page, total=total, css_framework="bootstrap4"
    )
    jsfilters = json.dumps(filters)
    return render_template(
        "thingstodo.html",
        city=location,
        things=suggestions,
        filters=filters,
        jsfilters=jsfilters,
        page=page,
        per_page=per_page,
        pagination=pagination,
        form=form,
        edit_form=edit_form,
        title="Things to do",
    )


@app.route("/delete/<city>/<suggestion>", methods=["POST"])
@login_required
def delete_suggestion(city, suggestion):
    """ Takes the values for city and suggestion passed in the url and uses
    them to locate the suggestion in the database. 'Pulls' the suggestion from
    the array it belongs to and flashes a message to the user to confirm the
    update. Returns user to the 'thingstodo' template """

    cities = mongo.db.cities
    cities.update_one(
        {"location": city},
        {"$pull": {"thingsToDo": {"suggestion": suggestion}}}
    )
    flash("Suggestion deleted.", "success")
    return redirect(url_for("suggestion_list", city=city))


@app.route("/edit/<city>/<suggestion>", methods=["POST"])
@login_required
def edit_suggestion(city, suggestion):
    """ Takes the values for city and suggestion passed in the url and uses
    them to locate the suggestion in the database. 'Pulls' the suggestion from
    the array it belongs to and flashes a message to the user to confirm the
    update. Returns user to the 'thingstodo' template """

    cities = mongo.db.cities
    cities.update_one(
        {"location": city},
        {"$pull": {"thingsToDo": {"suggestion": suggestion}}}
    )
    flash("Suggestion updated.", "success")
    return redirect(url_for("suggestion_list", city=city))