"""
reference: https://flask.palletsprojects.com/en/2.0.x/config/
           https://www.youtube.com/watch?v=GW_2O9CrnSU
"""

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SECRET_KEY = 'thisisdemo'

class Dev(Config):
    DEBUG = True

class Test(Config):
    TESTING = True

class Prod(Config):
    pass