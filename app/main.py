#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for,jsonify
from flask.globals import session
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy.orm import backref ,aliased
from forms import *
from flask_migrate import Migrate, migrate
from datetime import datetime
from sqlalchemy import func
import psycopg2

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    show = db.relationship('Show',backref='venue',lazy=True)


class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    show = db.relationship('Show',backref='artist',lazy=True)


class Show(db.Model):
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    artist_id = db.Column(db.Integer,db.ForeignKey('artist.id'))
    artist_name = db.Column(db.String)
    venue_id = db.Column(db.Integer,db.ForeignKey('venue.id'))
    venue_name = db.Column(db.String)
    starttime = db.Column(db.String(120))
    

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html' , venues=Venue.query.order_by(Venue.id.desc()).limit(10) ,artists=Artist.query.order_by(Artist.id.desc()).limit(10) )

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  z=0
  h=0
  results=[None]*len(Venue.query.all())
  venues=[None]*len(Venue.query.all())
  x=db.session.query(Venue.city,Venue.state).group_by(Venue.city,Venue.state).having(func.count('*')>1)
  for i,r in enumerate(x):
    h += 1
    y = Venue.query.filter_by(city=r.city,state=r.state).all()
    for l,k in enumerate(y):
      z += 1
      venues[l] = {"id":k.id,"name":k.name}
    results[h-1] = {"city":r.city,"state":r.state,"venues":venues}
    venues=[None]*len(Venue.query.all())

  x=db.session.query(Venue.city,Venue.state).group_by(Venue.city,Venue.state).having(func.count('*')==1)
  for i,r in enumerate(x):
    h += 1
    y = Venue.query.filter_by(city=r.city,state=r.state).all()
    for l,k in enumerate(y):
      z += 1
      venues[l] = {"id":k.id,"name":k.name}
    results[h-1] = {"city":r.city,"state":r.state,"venues":venues}
    venues=[None]*len(Venue.query.all())

  return render_template('pages/venues.html', areas=results )

@app.route('/venues/search', methods=['POST'])
def search_venues():
 
  y=True
  searchterm = request.form.get("search_term")
  result = Venue.query.all()
  response=[]
  for row in result:
   x=row.name.lower().find(searchterm.lower())
   if x != -1:
      response.append({'data':[{'id':row.id,"name":row.name}]})
      y=False
  if y==True:
     response=[]
 
  return render_template('pages/search_venues.html', results=response, search_term=searchterm)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  
  upcoming_shows=[]
  past_shows=[]
  shows=Show.query.filter_by(venue_id=venue_id).all()
  for show in shows:
    if show.starttime>str(datetime.today()):
      upcoming_shows.append(show)
    else:
      past_shows.append(show)
  return render_template('pages/show_venue.html', venue=Venue.query.get(venue_id) , upcoming_shows=upcoming_shows , past_shows=past_shows)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

  error =False
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    address = request.form.get('address')
    phone = request.form.get('phone')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    newvenue = Venue(name=name,city=city,state=state,address=address,phone=phone,genres=genres,facebook_link=facebook_link)
    db.session.add(newvenue)
    db.session.commit() 
    # sql = """INSERT INTO venue(id,name)
    #        VALUES(30,'mostafaa');"""
    # read database configuration
    # params = config()
    # connect to the PostgreSQL database 
    """ conn = psycopg2.connect(user="mostafa",
                                  password="root1234",
                                  host="postgresql-38627-0.cloudclusters.net",
                                  port="38656",
                                  database="fyyur") """
    """ conn = psycopg2.connect(user="aguekfdkrnfrhe",
                                  password="a94cee48d98b1013ce570a252765d81e63d418c77cc70ff78c3e62df6ba76bd4",
                                  host="ec2-52-5-1-20.compute-1.amazonaws.com",
                                  port="5432",
                                  database="d2doiu74e2s8o5") """
    # create a new cursor
    """ cur = conn.cursor()
    # execute the INSERT statement
    cur.execute(sql)
    # get the generated id back
    # vendor_id = cur.fetchone()[0]
    # commit the changes to the database
    conn.commit()
    # close communication with the database
    cur.close() """
  except:
     error= True
     db.session.rollback()
     flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  if not error:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

  error= False
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    error= True
    db.session.rollback()
  finally:
    db.session.close()

  return render_template('pages/home.html')

  

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():

  return render_template('pages/artists.html', artists=Artist.query.all())

@app.route('/artists/search', methods=['POST'])
def search_artists():
  y=True
  searchterm = request.form.get("search_term")
  result = Artist.query.all()
  response=[]
  for row in result:
   x=row.name.lower().find(searchterm.lower())
   if x != -1:
      response.append({'data':[{'id':row.id,"name":row.name}]})
      y=False
  if y==True:
     response=[]
  return render_template('pages/search_artists.html', results=response, search_term=searchterm)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  
  upcoming_shows=[]
  past_shows=[]
  shows=Show.query.filter_by(artist_id=artist_id).all()
  for show in shows:
    if show.starttime>str(datetime.today()):
      upcoming_shows.append(show)
    else:
      past_shows.append(show)
  return render_template('pages/show_artist.html', artist=Artist.query.get(artist_id), upcoming_shows=upcoming_shows , past_shows=past_shows)


@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):

  error= False
  try:
    Artist.query.filter_by(id=artist_id).delete()
    db.session.commit()
  except:
    error= True
    db.session.rollback()
  finally:
    db.session.close()

  return render_template('pages/home.html')


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  return render_template('forms/edit_artist.html', form=form, artist=Artist.query.get(artist_id))

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  error =False
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    edit = Artist.query.get(artist_id)
    edit.name=name
    edit.city=city
    edit.state=state
    edit.phone=phone
    edit.genres=genres
    edit.facebook_link=facebook_link
    db.session.commit()
  except:
     error= True
     db.session.rollback()
     flash('An error occurred. Artist ' + request.form['name'] + ' could not be edited.')
  finally:
    db.session.close()
  if not error:
    flash('Artist ' + request.form['name'] + ' was successfully edited!')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  return render_template('forms/edit_venue.html', form=form, venue=Venue.query.get(venue_id))

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error =False
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    address = request.form.get('address')
    phone = request.form.get('phone')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    edit = Venue.query.get(venue_id)
    edit.name=name
    edit.city=city
    edit.state=state
    edit.address=address
    edit.phone=phone
    edit.genres=genres
    edit.facebook_link=facebook_link
    db.session.commit()
  except:
     error= True
     db.session.rollback()
     flash('An error occurred. Venue ' + request.form['name'] + ' could not be edited.')
  finally:
    db.session.close()
  if not error:
    flash('Venue ' + request.form['name'] + ' was successfully edited!')
  return redirect(url_for('show_venue', venue_id=venue_id))

@app.route('/shows/<int:show_id>/edit', methods=['GET'])
def edit_show(show_id):
  form = ShowForm()
  
  return render_template('forms/edit_show.html', form=form, show=Show.query.get(show_id))

@app.route('/shows/<int:show_id>/edit', methods=['POST'])
def edit_show_submission(show_id):
  error =False
  try:
    name = request.form.get('name')
    artist_id = request.form.get('artist_id')
    artist_name = Artist.query.get(artist_id).name
    venue_id = request.form.get('venue_id')
    venue_name = Venue.query.get(venue_id).name
    starttime = request.form.get('start_time')
    edit = Show.query.get(show_id)
    edit.name=name
    edit.artist_id=artist_id
    edit.artist_name=artist_name
    edit.venue_id=venue_id
    edit.venue_name=venue_name
    edit.starttime=starttime
    db.session.commit()
  except:
     error= True
     db.session.rollback()
     flash('An error occurred. Show ' + request.form['name'] + ' could not be edited.')
  finally:
    db.session.close()
  if not error:
    flash('Show ' + request.form['name'] + ' was successfully edited!')

  return redirect(url_for('show_show', show_id=show_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error =False
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    newartist = Artist(name=name,city=city,state=state,phone=phone,genres=genres,facebook_link=facebook_link)
    db.session.add(newartist)
    db.session.commit()
  except:
     error= True
     db.session.rollback()
     flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  if not error:
    flash('Artist ' + request.form['name'] + ' was successfully listed!') 
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  return render_template('pages/shows.html', shows=Show.query.all())


@app.route('/shows/<int:show_id>')
def show_show(show_id):
  return render_template('pages/show_show.html', show=Show.query.get(show_id) )


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error =False
  x=False
  try:
    name = request.form.get('name')
    artist_id = request.form.get('artist_id')
    artist_name = Artist.query.get(artist_id).name
    venue_id = request.form.get('venue_id')
    venue_name = Venue.query.get(venue_id).name
    starttime = request.form.get('start_time')
    if Artist.query.get(artist_id) is not None and Venue.query.get(venue_id) is not None:
      newshow = Show(name=name,artist_id=artist_id,artist_name=artist_name,venue_id=venue_id,venue_name=venue_name,starttime=starttime)
      db.session.add(newshow)
      db.session.commit()
  except:
     error= True
     db.session.rollback()
     flash('An error occurred. Show could not be listed.')
     
  finally:
    db.session.close()
  if not error:
    flash('Show was successfully listed!')


  return render_template('pages/home.html')

@app.route('/shows/<show_id>', methods=['DELETE'])
def delete_show(show_id):

  error= False
  try:
    Show.query.filter_by(id=show_id).delete()
    db.session.commit()
  except:
    error= True
    db.session.rollback()
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.route('/shows/search', methods=['POST'])
def search_shows():
  
  y=True
  searchterm = request.form.get("search_term")
  result = Show.query.all()
  response=[]
  for row in result:
   x=row.name.lower().find(searchterm.lower())
   if x != -1:
      response.append({'data':[{'id':row.id,"name":row.name}]})
      y=False
  if y==True:
     response=[]
  return render_template('pages/search_shows.html', results=response, search_term=searchterm)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
""" if __name__ == '__main__':
    app.run() """

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
