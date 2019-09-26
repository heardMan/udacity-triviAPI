import os

#Set secret key for app
SECRET_KEY=os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True
TEST = None

# Connect to the database
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = '{}://{}@{}/{}'.format('postgresql', 'mark', 'localhost:5432', 'trivia')