from flask import Flask
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World"


if __name__ == "__main__":
    app.run(debug=true)