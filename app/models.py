from werkzeug.security import check_password_hash
from app import login_manager, mongo, app
from flask_login import LoginManager


class User():
    def __init__(self, _id, username, email):
        self._id = _id
        self.username = username
        self.email = email

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.email

    @staticmethod
    def check_password(hashed_password, password):
        return check_password_hash(hashed_password, password)


@login_manager.user_loader
def load_user(email):
    user = mongo.db.users.find_one({'email': email})
    if not user:
        return None
    return User(user['_id'], user['username'], user['email'])