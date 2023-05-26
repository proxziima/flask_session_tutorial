"""App configuration"""
from os import environ, path, system

import redis
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Set Flask configuration variables from .env file"""

    # General Config
    ENVIRONMENT = environ.get('ENVIRONMENT')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_DEBUG = environ.get('FLASK_DEBUG')
    SECRET_KEY = environ.get('SECRET_KEY')

    # Flask-Session
    REDIS_URI = environ.get("REDIS_URI")
    SESSION_TYPE = environ.get("SESSION_TYPE")
    SESSION_REDIS = redis.from_url(REDIS_URI)

    # Flask-Assets
    LESS_BIN = system("which lessc") # which lessc returns 0 if found in path else 1. This is a hacky way to check if lessc is installed
    ASSETS_DEBUG = environ.get('ASSETS_DEBUG')
    LESS_RUN_IN_DEBUG = environ.get('LESS_RUN_IN_DEBUG')

    # Static Assets
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    COMPRESSOR_DEBUG = environ.get('COMPRESSOR_DEBUG')

    # Flask-Sqlalchemy - Database
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
