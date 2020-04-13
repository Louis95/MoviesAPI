import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Database connection string
# SQLALCHEMY_DATABASE_URI = 'postgres://udacity@localhost:5432/movies'
SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]

# Supress warning
SQLALCHEMY_TRACK_MODIFICATIONS = False