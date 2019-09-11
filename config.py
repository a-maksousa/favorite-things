import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "key"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+mysqlconnector://admin:adminadmin@favoritesdb.c21zyakxlmwh.us-east-2.rds.amazonaws.com/favoritesdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False