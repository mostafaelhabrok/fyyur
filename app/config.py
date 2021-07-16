import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
#SQLALCHEMY_DATABASE_URI = 'postgresql://mostafa:root1234@postgresql-38627-0.cloudclusters.net:38656/fyyur'
SQLALCHEMY_DATABASE_URI = 'postgresql://aguekfdkrnfrhe:a94cee48d98b1013ce570a252765d81e63d418c77cc70ff78c3e62df6ba76bd4@ec2-52-5-1-20.compute-1.amazonaws.com:5432/d2doiu74e2s8o5'

