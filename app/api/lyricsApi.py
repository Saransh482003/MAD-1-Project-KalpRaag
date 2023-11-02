from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, marshal_with, reqparse, fields, abort
from app.models import db, Lyrics

api_lyrics = Blueprint("api_l", __name__)
api_l = Api(api_lyrics)

returner = {
    "lyrics_id": fields.Integer,
    "lyrics_path": fields.String,
    "song_id": fields.Integer,
}

lyrics_post = reqparse.RequestParser()
lyrics_post.add_argument("lyrics_path", type=str,help="Enter lyrics path", required=True)
lyrics_post.add_argument("song_id", type=int,help="Enter associated song id", required=True)

lyrics_put = reqparse.RequestParser()
lyrics_put.add_argument("lyrics_path", type=str,help="Enter lyrics path")
lyrics_put.add_argument("song_id", type=int,help="Enter associated song id")


class lyricsTransaction(Resource):
    @marshal_with(returner)
    def get(self):
        lyrics_id = request.args.get('id')
        lyrics_path = request.args.get('path')
        song_id = request.args.get('song_id')

        if lyrics_id:
            data = Lyrics.query.filter_by(lyrics_id=lyrics_id).first()
        elif lyrics_path:
            data = Lyrics.query.filter_by(lyrics_path=lyrics_path).first()
        elif song_id:
            data = Lyrics.query.filter_by(song_id=song_id).first()
        else:
            data = Lyrics.query.all()

        if data:
            return data, 200
        abort(400, message="Lyrics does not exist")


    @marshal_with(returner)
    def post(self):
        req = lyrics_post.parse_args()
        fetcher = Lyrics.query.filter_by(song_id=req["song_id"]).first()
        if (fetcher == None):
            lyricsEntry = Lyrics(
                lyrics_path=req["lyrics_path"],
                song_id=req["song_id"],
            )
            db.session.add(lyricsEntry)
            db.session.commit()
            fetcher = Lyrics.query.filter_by(song_id=req["song_id"]).first()
            return fetcher, 200
        abort(400, message="Lyrics Name exists.")

    @marshal_with(returner)
    def put(self):
        lyrics_id = request.args.get('id')
        lyrics_id = lyrics_id if lyrics_id!=None else ""
        req = lyrics_put.parse_args()
        fetcher = Lyrics.query.filter_by(lyrics_id=lyrics_id).first() 
        if fetcher:
            for i in req:
                setattr(fetcher,i,req[i])
            db.session.commit()
            fetcher = Lyrics.query.filter_by(lyrics_id=lyrics_id).first()
            return fetcher, 200
        abort(400, message="Lyrics do not exit")

    def delete(self):
        lyrics_id = request.args.get('id')
        lyrics_id = lyrics_id if lyrics_id!=None else ""
        fetcher = Lyrics.query.filter_by(lyrics_id=lyrics_id).first() 
        if fetcher:
            db.session.delete(fetcher)
            return {f"Song ID : {lyrics_id} deleted"}, 200
        abort(400, message="Lyrics do not exits")


api_l.add_resource(lyricsTransaction, "/")
