from flask import Flask
from .models import db
from .api.userApi import api_user
from .api.songsApi import api_songs
from .api.lyricsApi import api_lyrics
from .api.ratingApi import api_rating
from .api.playlistApi import api_playlist

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kalpRaag.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

db.init_app(app)

app.register_blueprint(api_user, url_prefix="/api/user")
app.register_blueprint(api_songs, url_prefix="/api/songs")
app.register_blueprint(api_lyrics, url_prefix="/api/lyrics")
app.register_blueprint(api_rating, url_prefix="/api/rating")
app.register_blueprint(api_playlist, url_prefix="/api/playlist")