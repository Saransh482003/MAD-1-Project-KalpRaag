from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, marshal_with, reqparse, fields, abort
from app.models import db, Album

api_album = Blueprint("api_a", __name__)
api_a = Api(api_album)

returner = {
    "album_id": fields.Integer,
    "album_name": fields.String,
    "genre": fields.String,
    "artist_id": fields.Integer,
    "creator_id": fields.Integer,
    "date_created": fields.String,
    "song_ids": fields.String,
    "saved_by": fields.String,
}

album_post = reqparse.RequestParser()
album_post.add_argument("album_name", type=str,help="Enter album_name", required=True)
album_post.add_argument("genre", type=str,help="Enter genre", required=True)
album_post.add_argument("artist_id", type=int,help="Enter artist_id", required=True)
album_post.add_argument("creator_id", type=int,help="Enter creator_id", required=True)
album_post.add_argument("date_created", type=str,help="Enter date_created", required=True)
album_post.add_argument("song_ids", type=str,help="Enter song_ids", required=True)
album_post.add_argument("saved_by", type=str,help="Enter saved_by", required=True)

album_put = reqparse.RequestParser()
album_put.add_argument("album_name", type=str,help="Enter album_name")
album_put.add_argument("genre", type=str,help="Enter genre")
album_put.add_argument("artist_id", type=int,help="Enter artist_id")
album_put.add_argument("creator_id", type=int,help="Enter creator_id")
album_put.add_argument("date_created", type=str,help="Enter date_created")
album_put.add_argument("song_ids", type=str,help="Enter song_ids")
album_put.add_argument("saved_by", type=str,help="Enter saved_by")


class albumTransaction(Resource):
    @marshal_with(returner)
    def get(self):
        album_id = request.args.get('album_id')
        album_name = request.args.get('album_name')
        genre = request.args.get('genre')
        artist_id = request.args.get('artist_id')
        creator_id = request.args.get('creator_id')
        date_created = request.args.get('date_created')
        song_ids = request.args.get('song_ids')
        saved_by = request.args.get('saved_by')

        if album_name and creator_id:
            data = Album.query.filter_by(album_name=album_name, creator_id=creator_id).first()
        else:
            if album_id:
                data = Album.query.filter_by(album_id=album_id).first()
            elif album_name:
                data = Album.query.filter_by(album_name=album_name).first()
            elif genre:
                data = Album.query.filter_by(genre=genre).all()
            elif artist_id:
                data = Album.query.filter_by(artist_id=artist_id).all()
            elif creator_id:
                data = Album.query.filter_by(creator_id=creator_id).all()
            elif date_created:
                data = Album.query.filter_by(date_created=date_created).all()
            elif song_ids:
                data = Album.query.filter_by(song_ids=song_ids).all()
            elif saved_by:
                data = Album.query.filter_by(saved_by=saved_by).all()
            else:
                data = Album.query.all()

        if data:
            return data, 200
        abort(400, message= "Album does not exist")


    @marshal_with(returner)
    def post(self):
        req = album_post.parse_args()
        fetcher = Album.query.filter_by(album_name=req["album_name"]).first()
        if (fetcher == None):
            albumEntry = Album(
                album_name=req["album_name"],
                genre=req["genre"],
                artist_id=req["artist_id"],
                creator_id=req["creator_id"],
                date_created=req["date_created"],
                song_ids=req["song_ids"],
                saved_by=req["saved_by"],
            )
            db.session.add(albumEntry)
            db.session.commit()
            fetcher = Album.query.filter_by(album_name=req["album_name"]).first()
            return fetcher, 200
        abort(400, message= "Album Name exists.")

    @marshal_with(returner)
    def put(self):
        req = album_put.parse_args()
        fetcher = Album.query.filter_by(album_name=req["album_name"]).first()
        if fetcher:
            for i in req:
                setattr(fetcher,i,req[i])
            db.session.commit()
            fetcher = Album.query.filter_by(album_name=req["album_name"]).first()
            return fetcher, 200
        abort(400, message= "Album do not exit")

    def delete(self):
        album_name = request.args.get('album_name')
        album_name = album_name if album_name!=None else ""
        fetcher = Album.query.filter_by(album_name=album_name).first()
        if fetcher:
            db.session.delete(fetcher)
            db.session.commit()
            return {f"Album Name : {album_name} deleted"}, 200
        abort(400, message= "Album do not exits")


api_a.add_resource(albumTransaction, "/")
