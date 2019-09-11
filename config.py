import os

class Config(object):
    strDevConnectionString = 'mysql+mysqlconnector://root:root@localhost/favoritesdb'
    strProdConnectionString = 'mysql+mysqlconnector://admin:adminadmin@favoritesdb.c21zyakxlmwh.us-east-2.rds.amazonaws.com/favoritesdb'
    SECRET_KEY = os.environ.get('SECRET_KEY') or "key"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or strDevConnectionString
    SQLALCHEMY_TRACK_MODIFICATIONS = False