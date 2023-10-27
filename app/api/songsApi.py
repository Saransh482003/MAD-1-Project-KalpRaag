from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, marshal_with, reqparse, fields, abort
from app.models import db, Songs

api_songs = Blueprint("api_s", __name__)
api_s = Api(api_songs)

returner = {
    "song_id": fields.Integer,
    "song_name": fields.String,
    "lyrics_id": fields.Integer,
    "duration": fields.Integer,
    "creator_id": fields.Integer,
    "artist_id": fields.Integer,
    "playlist_in": fields.Integer,
    "album_in": fields.Integer,
    "date_created": fields.String,
}

song_post = reqparse.RequestParser()
song_post.add_argument("song_name", type=str,
                       help="Enter song name", required=True)
song_post.add_argument("lyrics_id", type=int,
                       help="Enter song lyrics", required=True)
song_post.add_argument("duration", type=int,
                       help="Enter song duration", required=True)
song_post.add_argument("creator_id", type=int,
                       help="Enter song creator_id", required=True)
song_post.add_argument("artist_id", type=int,
                       help="Enter song artist_id", required=True)
song_post.add_argument("playlist_in", type=int,
                       help="Enter song playlist_in", required=True)
song_post.add_argument("album_in", type=int,
                       help="Enter song album_in", required=True)

song_put = reqparse.RequestParser()
song_put.add_argument("song_name", type=str, help="Enter song name")
song_put.add_argument("lyrics_id", type=int, help="Enter song lyrics")
song_put.add_argument("duration", type=int, help="Enter song duration")
song_put.add_argument("creator_id", type=int, help="Enter song creator_id")
song_put.add_argument("artist_id", type=int, help="Enter song artist_id")
song_put.add_argument("playlist_in", type=int, help="Enter song playlist_in")
song_put.add_argument("album_in", type=int, help="Enter song album_in")


class songTransaction(Resource):
    @marshal_with(returner)
    def get(self):
        song_id = request.args.get('id')
        song_name = request.args.get('name')
        lyrics_id = request.args.get('lyrics')
        creator_id = request.args.get('creator')
        artist_id = request.args.get('artist')
        playlist_in = request.args.get('playlist')
        album_in = request.args.get('album')
        date_created = request.args.get('date')

        if song_id:
            data = Songs.query.filter_by(song_id=song_id).first()
        elif song_name:
            data = Songs.query.filter_by(song_name=song_name).first()
        elif lyrics_id:
            data = Songs.query.filter_by(lyrics_id=lyrics_id).first()
        elif creator_id:
            data = Songs.query.filter_by(creator_id=creator_id).first()
        elif artist_id:
            data = Songs.query.filter_by(artist_id=artist_id).first()
        elif playlist_in:
            data = Songs.query.filter_by(playlist_in=playlist_in).first()
        elif album_in:
            data = Songs.query.filter_by(album_in=album_in).first()
        elif date_created:
            data = Songs.query.filter_by(date_created=date_created).first()
        else:
            data = Songs.query.all()

        if data:
            return data, 200
        abort(400, message="Song does not exist")


    @marshal_with(returner)
    def post(self):
        req = song_post.parse_args()
        fetcher = Songs.query.filter_by(song_name=req["song_name"]).first()
        if (fetcher == None):
            songEntry = Songs(
                song_name=req["song_name"],
                lyrics_id=req["lyrics_id"],
                duration=req["duration"],
                creator_id=req["creator_id"],
                artist_id=req["artist_id"],
                playlist_in=req["playlist_in"],
                album_in=req["album_in"],
                date_created=req["date_created"],
            )
            db.session.add(songEntry)
            db.session.commit()
            fetcher = Songs.query.filter_by(song_name=req["song_name"]).first()
            return fetcher, 200
        abort(400, message="Song Name exists.")

    @marshal_with(returner)
    def put(self):
        song_id = request.args.get('id')
        song_id = song_id if song_id!=None else ""
        req = song_put.parse_args()
        fetcher = Songs.query.filter_by(song_id=song_id).first() 
        if fetcher:
            for i in req:
                setattr(fetcher,i,req[i])
            fetcher = Songs.query.filter_by(song_id=song_id).first()
            return fetcher, 200
        abort(400, message="Song do not exit")

    def delete(self):
        song_id = request.args.get('id')
        song_id = song_id if song_id!=None else ""
        fetcher = Songs.query.filter_by(song_id=song_id).first() 
        if fetcher:
            db.session.delete(fetcher)
            return {f"Song ID : {song_id} deleted"}, 200
        abort(400, message="Song do not exits")


api_s.add_resource(songTransaction, "/")
