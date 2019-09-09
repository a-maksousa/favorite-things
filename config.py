import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "key"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+mysqlconnector://root:root@localhost/favorites'
    SQLALCHEMY_TRACK_MODIFICATIONS = False