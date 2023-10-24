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
