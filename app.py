#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

#____________________________________________
import sys
import random
from flask_migrate import Migrate
from models import db

from models import Venue, Artist, Show
#____________________________________________
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
# db = SQLAlchemy(app)

db.init_app(app)

migrate = Migrate(app, db)

# TODO: connect to a local postgresql database




#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

  data = Venue.query.all()
  print(data)

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():

  search_item =request.form.get('search_term', ' ')
  searched_venues = Venue.query.filter(Venue.name.ilike(f"%{search_item}%")).all()
  print(searched_venues)
  count = len(searched_venues)
  
  response={
    "count": count,
    "data": searched_venues
  }
  
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

  venue = Venue.query.filter(Venue.id == venue_id).all()
  print(f"\n\n from show artists\n\n{venue_id} \n{venue}\n\n")

  if venue == None:
    abort(404)

  return render_template('pages/show_venue.html', venue=venue[0])

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

  r = random.randint(100,500)
  fv = VenueForm(request.form)
  
  try:
    venue = Venue(id=r, name=fv.name.data, city=fv.city.data, state=fv.state.data, phone=fv.phone.data, genres=fv.genres.data, facebook_link=fv.facebook_link.data, image_link=fv.image_link.data, seeking_talent=fv.seeking_talent.data, seeking_description=fv.seeking_description.data)
    db.session.add(venue)
    db.session.commit()
  
  # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except:
    db.session.rollback()
    flash('An error occured! Venue ' + request.form['name'] +' could not be listed.')
    print("create_venue_submission() ", sys.exc_info(), "\n\n")
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    Venue.query.filter_by(id = venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
    abort(404)
  finally:
    db.session.close()

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.all()
  print(f"\n\nArtist:\n{data}\n\n")
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_item =request.form.get('search_term', ' ')
  searched_artist = Artist.query.filter(Artist.name.ilike(f"%{search_item}%")).all()
  print(searched_artist)
  count = len(searched_artist)
  
  response={
    "count": count,
    "data": searched_artist
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.filter(Artist.id == artist_id).all()
  print(f"\n\n from show artists\n\n{artist_id} \n{artist}\n\n")

  if artist == None:
    abort(404)

  return render_template('pages/show_artist.html', artist=artist[0])

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist_update = Artist.query.filter(Artist.id == artist_id).first()
  artist_update = vars(artist_update)
  print(f"\n\n\n{artist_update}\n\n\n") # Debugging
  print(type(artist_update)) # Debugging

  if artist_update == None:
    print(f"\n\n\nError | Abort 404\n\n\n")
    abort(404)

  form = ArtistForm(data=artist_update)
  return render_template('forms/edit_artist.html', form=form, artist=artist_update)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # fa - - artist form
  fa = ArtistForm(request.form)
  try:
    artist = Artist.query.filter_by(id=artist_id).first()
    artist.name = fa.name.data
    artist.city = fa.city.data
    artist.state = fa.state.data
    artist.phone = fa.phone.data
    artist.genre = fa.genres.data
    artist.facebook_link = fa.facebook_link.data
    artist.image_link = fa.image_link.data
    artist.website = fa.website_link.data
    artist.seeking_venue = fa.seeking_venue
    artist.seeking_description = fa.seeking_description

    print(f"\n\n\n{artist}\n\n\n") # Debugging
    print("Typeof artist", type(artist)) # Debugging

    db.session.commit()
    flash("Success")
  except:
    db.session.rollback()
    #Debugging
    print(f"\n\n\nError\n\n\n")
    print(sys.exc_info())
    flash("An error occured!"+ artist.name + " could not be updated")
  finally:
    db.session.close()  

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue_update = Venue.query.filter(Venue.id == venue_id).first()
  venue_update = vars(venue_update)
  print(f"\n\n\n{venue_update}\n\n\n") # Debugging
  print(type(venue_update)) # Debugging

  if venue_update == None:
    print(f"\n\n\nError | Abort 404\n\n\n")
    abort(404)

  form = VenueForm(data=venue_update)

  return render_template('forms/edit_venue.html', form=form, venue=venue_update)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # va - - venue form
  va = VenueForm(request.form)
  try:
    venue = Venue.query.filter_by(id=venue_id).first()
    venue.name = va.name.data
    venue.city = va.city.data
    venue.state = va.state.data
    venue.phone = va.phone.data
    venue.genre = va.genres.data
    venue.facebook_link = va.facebook_link.data
    venue.image_link = va.image_link.data
    venue.website = va.website_link.data
    venue.seeking_talent = va.seeking_talent.data
    venue.seeking_description = va.seeking_description.data

    print(f"\n\n\n{venue}\n\n") # Debugging
    print("Typeof artist", type(venue)) # Debugging

    db.session.commit()
    flash("Success")
  except:
    db.session.rollback()
    #Debugging
    print(f"\n\n\nError\n")
    print(sys.exc_info())
    flash("An error occured! "+ venue.name + " could not be updated")
  finally:
    db.session.close() 


  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  random_integer = random.randint(100,500)
  #fa -- artist form
  fa = ArtistForm(request.form)
  
  try:
    artist = Artist(id=random_integer, name=fa.name.data, city=fa.city.data, state=fa.state.data, phone=fa.phone.data, genres=fa.genres.data, facebook_link=fa.facebook_link.data, image_link=fa.image_link.data, seeking_venue=fa.seeking_venue.data, seeking_description=fa.seeking_description.data, website=fa.website_link.data)
    db.session.add(artist)
    db.session.commit()
  
  # on successful db insert, flash success
    flash('Arists: ' + request.form['name'] + ' was successfully listed!')

  except:
    db.session.rollback()
    flash('An error occured! Artist: ' + request.form['name'] +' could not be listed.')
    print("\n\n" + sys.exc_info() + "\n\n")
  finally:
    db.session.close()

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data = Show.query.all()

  for show in data:
    show.start_time = str(show.start_time)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  random_integer = random.randint(0, 100)
  sf = ShowForm(request.form)
  try:
    show = Show(id = random_integer, venue_id=sf.venue_id.data, artist_id=sf.artist_id.data, start_time=sf.start_time.data)
    db.session.add(show)
    db.session.commit()
  except:
    db.session.rollback()
    flash("An error occured! Show: " + request.form['name'] + " could not be listed.")
    #debugging
    print("\n\nError\ncreate_show_submission():" + sys.exc_info() + "\n\n")
  finally:
    db.session.close()

  return render_template('pages/home.html')

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
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
