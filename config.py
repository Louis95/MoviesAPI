import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Database connection string
# SQLALCHEMY_DATABASE_URI = 'postgres://udacity@localhost:5432/movies'
SQLALCHEMY_DATABASE_URI = 'postgres://mizkaqudrvclaq:83ff9158a9332ddcab66f03a3a387c64554f49e916a1746d840e3c067818dad4@ec2-52-6-143-153.compute-1.amazonaws.com:5432/dckkrj3786hpta'

# Supress warning
SQLALCHEMY_TRACK_MODIFICATIONS = False