import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgres://ycfcabbluttfcy:287eec2cb091c2ff866463b0c561e0c48e8eac6950c2583a5d828f57c0d3b9d8@ec2-35-171-250-21.compute-1.amazonaws.com:5432/dd1rlv4266ss22
'
