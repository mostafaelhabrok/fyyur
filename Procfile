web: gunicorn --bind 0.0.0.0:$PORT app:app
init: python app.py db init
migrate: python app.py db migrate
upgrade: python app.py db upgrade