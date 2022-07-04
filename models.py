from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # Implements mimssing fields as a database migration
    genres = db.Column(db.String)
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    website = db.Column(db.String)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    # shows = db.relationship('Venue', backref='Venue', lazy='dynamic')
    
    def __repr__(self):
      return f'<Venue {self.id} {self.name} {self.city} {self.state} {self.address} {self.phone} {self.image_link} {self.facebook_link} {self.genres} {self.seeking_talent} {self.seeking_description} { self.website}>'

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    address = db.Column(db.String(120))

    website = db.Column(db.String)
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    seeking_talent = db.Column(db.String)

    venue = db.relationship('Venue', backref='Artist', lazy='dynamic')
    # show = db.relationship('Show', backref='Artist', lazy='dynamic')
    
    def __repr__(self):
      return f'<Artist {self.id} {self.name} {self.city} {self.state} {self.address} {self.phone} {self.image_link} {self.facebook_link} {self.genres} {self.seeking_talent} {self.seeking_description} { self.website}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# Implements show models and complete migrations
class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.String)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  venue = db.relationship('Venue', backref='Show', lazy='joined')
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  artist = db.relationship('Artist', backref='Show', lazy='joined')

  def __repr__(self):
    return f'<Shows {self.id} {self.start_time} {self.venue_id} {self.venue} {self.artist_id} {self.artist}>'
