import os
from flask import Flask
from flask_pymongo import PyMongo
from config import Config

app = Flask(__name__)

app.config.from_object(Config)
app.config['MONGO_URI'] = Config.MONGO_URI
mongo = PyMongo(app)

from app import routes