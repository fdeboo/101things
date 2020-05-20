import os
from flask import Flask
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from config import Config

app = Flask(__name__)

app.config.from_object(Config)


from app import routes