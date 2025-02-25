import os

class config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLACHEMY_DATABASE_URI = 'sqlite:///site.db'
    SECRET_KEY = os.urandom(24)