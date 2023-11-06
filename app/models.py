from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String, unique=True, nullable=False)
    user_password = db.Column(db.String, nullable=False)
    creator_id = db.Column(db.Integer, nullable=True, unique=True)
    playlists = db.Column(db.String,nullable=True)

class Songs(db.Model):
    song_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song_name = db.Column(db.String, nullable=False)
    lyrics_id = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    creator_id = db.Column(db.Integer, nullable=False)
    artist_id = db.Column(db.Integer, nullable=False)
    playlist_in = db.Column(db.Integer, nullable=False)
    album_in = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.String, nullable=False)

class Lyrics(db.Model):
    lyrics_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lyrics_path = db.Column(db.String, nullable=False)
    song_id = db.Column(db.Integer, nullable=False)

class Rating(db.Model):
    s_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    love = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String,nullable=False)
    __table_args__ = (db.UniqueConstraint('song_id', 'user_name', name='song_user_unique'),)