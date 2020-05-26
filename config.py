import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGO_URI = os.environ.get('MONGO_URI')
    CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')    
    cloudinary.config(
        cloud_name= os.environ.get('CLOUDINARY_CLOUD_NAME'),
        api_key = os.environ.get('CLOUDINARY_API_KEY'),
        api_secret = os.environ.get('CLOUDINARY_API_SECRET')
    )
    DEBUG = True