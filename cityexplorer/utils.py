import os
from flask import url_for, render_template
from flask_mail import Message
from cityexplorer import mail
from cityexplorer.models import User


def send_reset_email(user):
    this_user = User(
        user["_id"],
        user["username"],
        user["fname"],
        user["lname"],
        user["email"],
    )
    token = this_user.get_reset_token()
    msg = Message(
        "Password Reset Request",
        sender=os.environ.get("EMAIL_USER"),
        recipients=[user["email"]],
    )
    msg.body = f"""To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes
will be made.
"""
    msg.html = render_template(
        "reset_email.html", username=this_user, token=token
    )

    mail.send(msg)


def skiplimit(page_num, query, limit):
    skips = limit * (page_num - 1)
    cursor = query.sort('location').skip(skips).limit(limit)
    return cursor
