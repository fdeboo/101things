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
    EditSuggestionForm,
    SearchLocationForm,
    FilterResultsForm,
    UploadImageForm,
)
from cityexplorer import app, mongo
from cityexplorer.utils import send_reset_email

CITIES = mongo.db.cities
USERS = mongo.db.users


@app.before_request
def before_request_func():
    """ Instantiates the SearchLocationForm so that it can be
    accessed globally in the app """

    g.searchform = SearchLocationForm()
    g.editsuggestion = EditSuggestionForm()
    g.updateimage = UploadImageForm()


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def index():
    """ If a search term is submitted, queries the database for case-
    insensitive matches. Otherwise, queries the database for all documents.

    Passes the results to the template in a limited batch so that large numbers
    of results are divided over several pages and are paginated.
    Displays results for all locations in the database """

    searched = ""
    page, per_page, offset = get_page_args(
        page_parameter="page", per_page_parameter="per_page"
    )
    per_page = 4
    offset = (page - 1) * per_page
    if g.searchform.validate_on_submit():
        searched = g.searchform.q.data
        query = CITIES.find(
            {"location": {"$regex": searched, "$options": "i"}}
        )
    else:
        query = CITIES.find({})
        if CITIES.find(
                {
                    "$or": [
                        {"thingsToDo": {"$exists": False}},
                        {"thingsToDo": {"$size": 0}},
                    ]
                }
        ):

            CITIES.delete_many({"thingsToDo": {"$exists": False}})
            CITIES.delete_many({"thingsToDo": {"$size": 0}})
    total = query.count()
    locations = query[offset: offset + per_page]
    pagination = Pagination(
        page=page, per_page=per_page, total=total, css_framework="bootstrap4"
    )
    suggestion_query = CITIES.aggregate(
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
    return render_template(
        "pages/home.html",
        locations=locations,
        searched=searched,
        suggestions=suggestion_query,
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
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        USERS.insert(
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
                "is_admin": False,
            }
        )
        flash("You are now registered and can log in", "success")
        return redirect(url_for("login"))
    return render_template("pages/register.html", form=form, title="Register")


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Checks if the current user is already signed in and if so, redirects
    them to the home page.

    Instantiates the Login form and when submitted, searches the database for
    a record matching the inputted data in the form email field. Hashes the
    password using the function from werkzeug.security and checks it against
    the password for the user in the database.

    If the passwords match, the User object is instantiated with the properties
    of the user in the database

    Logs in the user and sends them to the page they were trying to access
    (if applicable), else redirects them to the home page """

    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = USERS.find_one({"email": form.email.data.lower()})
        if user and check_password_hash(user["password"], form.password.data):
            user_data = User(
                user["_id"],
                user["username"],
                user["fname"],
                user["lname"],
                user["email"],
                user["picture"],
                user["is_admin"],
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
    return render_template("pages/login.html", form=form, title="Login")


@app.route("/logout")
def logout():
    """ Logs the user out using logout_user function from flask_login and
    redirects them to the home page """

    logout_user()
    return redirect(url_for("index"))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """" image_url is the name provided for the first parameter of the
    cloudinary upload options is provided as a name for the dictionary
    of options giving both parameters a variable name keeps the url
    string separate """

    form = UpdateAccountForm()
    user = USERS.find_one({"username": current_user.username})
    if form.validate_on_submit():
        if form.picture.data:
            print(form.picture.data)
            uploaded_image = upload(
                form.picture.data,
                folder="profile_pics",
                format="jpg",
                width=150,
                height=150,
            )
            image_url, options = cloudinary_url(uploaded_image["public_id"])

        else:
            image_url = user["picture"]
        USERS.update_one(
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
    query = ""
    page, per_page, offset = get_page_args(
        page_parameter="page", per_page_parameter="per_page"
    )
    query = CITIES.aggregate(
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
                    "location": "$location",
                    "suggestion": "$thingsToDo.suggestion",
                    "cost": "$thingsToDo.cost",
                    "category": "$thingsToDo.category",
                    "url": "$thingsToDo.url",
                    "comment": "$thingsToDo.comment",
                    "author": "$thingsToDo.author",
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
    return render_template(
        "pages/account.html",
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
        user = USERS.find_one({"email": form.email.data})
        send_reset_email(user)
        flash(
            "An email has been sent with instructions to reset your password.",
            "info",
        )
        return redirect(url_for("login"))
    return render_template(
        "pages/reset_request.html", title="Reset Password", form=form
    )


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    """ Description """
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "danger")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        USERS.update_one(
            {"email": user["email"]}, {"$set": {"password": hashed_password}}
        )
        flash(
            "Your password has been updated! You are now able to log in",
            "success",
        )
        return redirect(url_for("login"))
    return render_template(
        "pages/reset_token.html", title="Reset Password", form=form
    )


@app.route("/delete/<user>", methods=["POST"])
@login_required
def delete_account(user):
    """ Takes the value for user passed in the url and uses it in the db query
    to locate the user in the database. Deletes the user object from the db,
    Flashes a message to the user to confirm the deletion. Returns user to the
    'home' template """

    USERS.delete_one({"username": user})
    flash("Account deleted.", "success")
    return redirect(url_for("index"))


# Places routes
@app.route("/addlocation", methods=["GET", "POST"])
@login_required
def add_location():
    """ Instantiates the Location form. Inserts a new document using data
    retrieved from the form input """

    form = CreateLocationForm()
    if form.validate_on_submit():
        CITIES.insert_one(
            {"location": form.location.data, "bg_img": form.image.data}
        )
        location = form.location.data
        return redirect(url_for("add_suggestion", location=location))
    return render_template("pages/addlocation.html", form=form, title="Add Location")


@app.route("/addsuggestion/<location>", methods=["GET", "POST"])
@login_required
def add_suggestion(location):
    """ Instanstiates the suggestion form. Updates the database using the
    data retrieved from the form input. Redirects to the thingsToDo template.
    """

    form = CreateSuggestionForm()
    if form.validate_on_submit():
        CITIES.update(
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
        "pages/addsuggestion.html",
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
    location = CITIES.find_one(
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
            query = CITIES.aggregate(
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
                    {
                        "$unwind": {
                            "path": "$user_profile",
                            "preserveNullAndEmptyArrays": True,
                        }
                    },
                    {
                        "$project": {
                            "location": "$location",
                            "suggestion": "$thingsToDo.suggestion",
                            "cost": "$thingsToDo.cost",
                            "category": "$thingsToDo.category",
                            "url": "$thingsToDo.url",
                            "comment": "$thingsToDo.comment",
                            "author": "$thingsToDo.author",
                            "profile": "$user_profile.picture",
                        }
                    },
                ]
            )
        elif len(condition_a) == 0:
            query = CITIES.aggregate(
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
                    {
                        "$unwind": {
                            "path": "$user_profile",
                            "preserveNullAndEmptyArrays": True,
                        }
                    },
                    {
                        "$project": {
                            "location": "$location",
                            "suggestion": "$thingsToDo.suggestion",
                            "cost": "$thingsToDo.cost",
                            "category": "$thingsToDo.category",
                            "url": "$thingsToDo.url",
                            "comment": "$thingsToDo.comment",
                            "author": "$thingsToDo.author",
                            "profile": "$user_profile.picture",
                        }
                    },
                ]
            )

        else:
            query = CITIES.aggregate(
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
                    {
                        "$unwind": {
                            "path": "$user_profile",
                            "preserveNullAndEmptyArrays": True,
                        }
                    },
                    {
                        "$project": {
                            "location": "$location",
                            "suggestion": "$thingsToDo.suggestion",
                            "cost": "$thingsToDo.cost",
                            "category": "$thingsToDo.category",
                            "url": "$thingsToDo.url",
                            "comment": "$thingsToDo.comment",
                            "author": "$thingsToDo.author",
                            "profile": "$user_profile.picture",
                        }
                    },
                ]
            )

    else:
        query = CITIES.aggregate(
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
                {
                    "$unwind": {
                        "path": "$user_profile",
                        "preserveNullAndEmptyArrays": True,
                    }
                },
                {
                    "$project": {
                        "location": "$location",
                        "suggestion": "$thingsToDo.suggestion",
                        "cost": "$thingsToDo.cost",
                        "category": "$thingsToDo.category",
                        "url": "$thingsToDo.url",
                        "comment": "$thingsToDo.comment",
                        "author": "$thingsToDo.author",
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
        "pages/thingstodo.html",
        city_obj=location,
        things=suggestions,
        filters=filters,
        jsfilters=jsfilters,
        page=page,
        per_page=per_page,
        pagination=pagination,
        form=form,
        title="Things to do",
    )


@app.route("/delete/location/<city>", methods=["POST"])
@login_required
def delete_location(city):
    """ Takes the value of 'city' passed in the url and uses it to identify the
    document in the database. Deletes the document from
    the array it belongs to and flashes a message to the user to confirm the
    update. If the url contains a value for 'author, (the user routed from
    their account page) redirect to account template. Else, (the user routed
    from the thingstodo page) redirect to thingstodo template.  """
    CITIES.delete_one({"location": city})
    flash("Suggestion deleted.", "success")
    return redirect(url_for("index"))


@app.route("/edit/location/<city>", methods=["POST"])
@login_required
def upload_image(city):
    """ Takes the value of 'city' passed in the url and uses it to identify the
    document in the database.  flashes a message to the user to confirm the
    update. If the url contains a value for 'author, (the user routed from
    their account page) redirect to account template. Else, (the user routed
    from the thingstodo page) redirect to thingstodo template.  """

    print('directed successfully')
    if g.updateimage.validate_on_submit():
        uploaded_image = upload(
            g.updateimage.image.data,
            folder="locations",
            format="jpg",
        )
        image_url, options = cloudinary_url(uploaded_image["public_id"])
        CITIES.update_one(
            {"location": city},
            {"$set": {"bg_img": image_url}},
            )
        flash("Image Updated.", "success")
        return redirect(url_for("index"))
    else:
        flash("Unsuccessful.", "danger")
        return redirect(url_for("index"))


@app.route("/delete/suggestion/<city>/<suggestion>", methods=["POST"])
@app.route("/delete/suggestion/<city>/<suggestion>/<author>", methods=["POST"])
@login_required
def delete_suggestion(city, suggestion, author=None):
    """ Takes the values for city and suggestion passed in the url and uses
    them to locate the suggestion in the database. 'Pulls' the suggestion from
    the array it belongs to and flashes a message to the user to confirm the
    update. If the url contains a value for 'author, (the user routed from
    their account page) redirect to account template. Else, (the user routed
    from the thingstodo page) redirect to thingstodo template.  """

    CITIES.update_one(
        {"location": city},
        {"$pull": {"thingsToDo": {"suggestion": suggestion}}},
    )
    flash("Suggestion deleted.", "success")
    if author is not None:
        return redirect(url_for("account"))
    return redirect(url_for("suggestion_list", city=city))


@app.route("/edit/suggestion/<city>", methods=["POST"])
@app.route("/edit/suggestion/<author>/<city>", methods=["POST"])
@login_required
def edit_suggestion(city, author=None):
    """ Takes the values for city and suggestion passed in the url and uses
    them to locate the suggestion object in the database. 'Sets' the object's
    field values with the data submitted in the editsuggestion form. Flashes a
    message to the user to confirm the update. If the url contains a value for
    'author, (the user routed from their account page) redirect to account
    template. Else, (the user routed from the thingstodo page) redirect to
    thingstodo template. """

    if g.editsuggestion.validate_on_submit():
        suggestion = g.editsuggestion.suggestion.data
        CITIES.update(
            {"location": city, "thingsToDo.suggestion": suggestion},
            {
                "$set": {
                    "thingsToDo.$": {
                        "suggestion": g.editsuggestion.suggestion.data,
                        "category": g.editsuggestion.category.data,
                        "cost": g.editsuggestion.cost.data,
                        "url": g.editsuggestion.url.data,
                        "comment": g.editsuggestion.comment.data,
                        "author": current_user.username,
                    }
                }
            },
        )
        flash("Suggestion updated.", "success")
        if author is not None:
            return redirect(url_for("account"))
        return redirect(url_for("suggestion_list", city=city))

    flash("Update unsuccessful.", "danger")
    if author is not None:
        return redirect(url_for("account"))
    return redirect(url_for("suggestion_list", city=city))
