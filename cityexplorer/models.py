from werkzeug.security import check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from cityexplorer import login_manager, mongo, app
from flask_login import LoginManager


class User():
    def __init__(self, _id, username, fname, lname, email):
        self._id = _id
        self.username = username
        self.fname = fname
        self.lname = lname
        self.email = email

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.username

    @staticmethod
    def check_password(hashed_password, password):
        return check_password_hash(hashed_password, password)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'email': self.email})


@login_manager.user_loader
def load_user(username):
    user = mongo.db.users.find_one({'username': username})
    if not user:
        return None
    return User(user['_id'], user['username'], user['fname'], user['lname'], user['email'])