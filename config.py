import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGO_URI = os.environ.get('MONGO_URI')
    CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL_USER')
    MAIL_PASSWORD = os.getenv('EMAIL_PASS')    
    DEBUG = True