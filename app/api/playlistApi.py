from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, marshal_with, reqparse, fields, abort
from app.models import db, Playlist

api_playlist = Blueprint("api_p", __name__)
api_p = Api(api_playlist)

returner = {
    "playlist_id": fields.Integer,
    "playlist_name": fields.String,
    "user_name": fields.String,
    "song_ids": fields.String,
}

playlist_post = reqparse.RequestParser()
playlist_post.add_argument("playlist_name", type=str,help="Enter playlist name", required=True)
playlist_post.add_argument("user_name", type=str,help="Enter user name", required=True)
playlist_post.add_argument("song_ids", type=str,help="Enter song_ids", required=True)

playlist_put = reqparse.RequestParser()
playlist_put.add_argument("playlist_name", type=str,help="Enter playlist name")
playlist_put.add_argument("user_name", type=str,help="Enter user name")
playlist_put.add_argument("song_ids", type=str,help="Enter song_ids")


class playlistTransaction(Resource):
    @marshal_with(returner)
    def get(self):
        playlist_id = request.args.get('playlist_id')
        playlist_name = request.args.get('playlist_name')
        user_name = request.args.get('user_name')
        song_ids = request.args.get('song_ids')

        if playlist_name and user_name:
            data = Playlist.query.filter_by(playlist_name=playlist_name, user_name=user_name).first()
        else:
            if playlist_id:
                data = Playlist.query.filter_by(playlist_id=playlist_id).first()
            elif playlist_name:
                data = Playlist.query.filter_by(playlist_name=playlist_name).all()
            elif user_name:
                data = Playlist.query.filter_by(user_name=user_name).all()
            else:
                data = Playlist.query.all()

        if data:
            return data, 200
        abort(400, message= "Playlist does not exist")


    @marshal_with(returner)
    def post(self):
        req = playlist_post.parse_args()
        fetcher = Playlist.query.filter_by(playlist_name=req["playlist_name"],user_name=req["user_name"]).first()
        if (fetcher == None):
            playlistEntry = Playlist(
                playlist_name=req["playlist_name"],
                user_name=req["user_name"],
                song_ids=req["song_ids"],
            )
            db.session.add(playlistEntry)
            db.session.commit()
            fetcher = Playlist.query.filter_by(playlist_name=req["playlist_name"],user_name=req["user_name"]).first()
            return fetcher, 200
        abort(400, message= "Playlist Name exists.")

    @marshal_with(returner)
    def put(self):
        req = playlist_put.parse_args()
        fetcher = Playlist.query.filter_by(playlist_name=req["playlist_name"],user_name=req["user_name"]).first()
        if fetcher:
            for i in req:
                setattr(fetcher,i,req[i])
            db.session.commit()
            fetcher = Playlist.query.filter_by(playlist_name=req["playlist_name"],user_name=req["user_name"]).first()
            return fetcher, 200
        abort(400, message= "Playlist do not exit")

    def delete(self):
        playlist_name = request.args.get('playlist_name')
        user_name = request.args.get('user_name')
        playlist_name = playlist_name if playlist_name!=None else ""
        user_name = user_name if user_name!=None else ""
        fetcher = Playlist.query.filter_by(playlist_name=playlist_name,user_name=user_name)
        if fetcher:
            for i in fetcher:
                db.session.delete(i)
            db.session.commit()
            return {f"Playlist Name : {playlist_name} for User : {user_name} deleted"}, 200
        abort(400, message= "Playlist do not exits")


api_p.add_resource(playlistTransaction, "/")
