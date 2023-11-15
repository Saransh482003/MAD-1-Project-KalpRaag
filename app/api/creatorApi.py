from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, marshal_with, reqparse, fields, abort
from app.models import db, Creator

api_creator = Blueprint("api_c", __name__)
api_c = Api(api_creator)

returner = {
    "creator_id": fields.Integer,
    "user_name": fields.String,
    "song_ids": fields.String,
    "album_ids": fields.String,
}

creator_post = reqparse.RequestParser()
creator_post.add_argument("user_name", type=str,help="Enter album_name", required=True)
creator_post.add_argument("song_ids", type=str,help="Enter genre", required=True)
creator_post.add_argument("album_ids", type=str,help="Enter artist_id", required=True)

creator_put = reqparse.RequestParser()
creator_put.add_argument("user_name", type=str,help="Enter album_name")
creator_put.add_argument("song_ids", type=str,help="Enter genre")
creator_put.add_argument("album_ids", type=str,help="Enter artist_id")


class creatorTransaction(Resource):
    @marshal_with(returner)
    def get(self):
        creator_id = request.args.get('creator_id')
        user_name = request.args.get('user_name')
        song_ids = request.args.get('song_ids')
        album_ids = request.args.get('album_ids')

        if creator_id:
            data = Creator.query.filter_by(creator_id=creator_id).first()
        elif user_name:
            data = Creator.query.filter_by(user_name=user_name).first()
        elif song_ids:
            data = Creator.query.filter_by(song_ids=song_ids).all()
        elif album_ids:
            data = Creator.query.filter_by(album_ids=album_ids).all()
        else:
            data = Creator.query.all()

        if data:
            return data, 200
        abort(400, message= "Creator does not exist")


    @marshal_with(returner)
    def post(self):
        req = creator_post.parse_args()
        fetcher = Creator.query.filter_by(user_name=req["user_name"]).first()
        if (fetcher == None):
            creatorEntry = Creator(
                user_name=req["user_name"],
                song_ids=req["song_ids"],
                album_ids=req["album_ids"],
            )
            db.session.add(creatorEntry)
            db.session.commit()
            fetcher = Creator.query.filter_by(user_name=req["user_name"]).first()
            return fetcher, 200
        abort(400, message= "Creator Name exists.")

    @marshal_with(returner)
    def put(self):
        req = creator_put.parse_args()
        fetcher = Creator.query.filter_by(user_name=req["user_name"]).first()
        if fetcher:
            for i in req:
                setattr(fetcher,i,req[i])
            db.session.commit()
            fetcher = Creator.query.filter_by(user_name=req["user_name"]).first()
            return fetcher, 200
        abort(400, message= "Creator do not exit")

    def delete(self):
        user_name = request.args.get('user_name')
        user_name = user_name if user_name!=None else ""
        fetcher = Creator.query.filter_by(user_name=user_name).first()
        if fetcher:
            db.session.delete(fetcher)
            db.session.commit()
            return {f"Creator Name : {user_name} deleted"}, 200
        abort(400, message= "Creator do not exits")


api_c.add_resource(creatorTransaction, "/")
