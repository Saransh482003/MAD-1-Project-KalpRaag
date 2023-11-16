from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, marshal_with, reqparse, fields, abort
from app.models import db, Artists

api_artists = Blueprint("api_ar", __name__)
api_ar = Api(api_artists)

returner = {
    "artist_id": fields.Integer,
    "artist_name": fields.String,
}

artist_post = reqparse.RequestParser()
artist_post.add_argument("artist_name", type=str,help="Enter artist_name", required=True)

artist_put = reqparse.RequestParser()
artist_put.add_argument("album_name", type=str,help="Enter artist_name")


class artistTransaction(Resource):
    @marshal_with(returner)
    def get(self):
        artist_id = request.args.get('artist_id')
        artist_name = request.args.get('artist_name')

        if artist_id:
            data = Artists.query.filter_by(artist_id=artist_id).first()
        elif artist_name:
            data = Artists.query.filter_by(artist_name=artist_name).first()
        else:
            data = Artists.query.all()

        if data:
            return data, 200
        abort(400, message= "Artists does not exist")


    @marshal_with(returner)
    def post(self):
        req = artist_post.parse_args()
        fetcher = Artists.query.filter_by(artist_name=req["artist_name"]).first()
        if (fetcher == None):
            artistsEntry = Artists(
                artist_name=req["artist_name"],
            )
            db.session.add(artistsEntry)
            db.session.commit()
            fetcher = Artists.query.filter_by(artist_name=req["artist_name"]).first()
            return fetcher, 200
        abort(400, message= "Artists Name exists.")

    @marshal_with(returner)
    def put(self):
        args = request.args.get('artist_name')
        req = artist_put.parse_args()
        fetcher = Artists.query.filter_by(artist_name=args).first()
        if fetcher:
            for i in req:
                setattr(fetcher,i,req[i])
            db.session.commit()
            fetcher = Artists.query.filter_by(artist_id=fetcher.artist_id).first()
            return fetcher, 200
        abort(400, message= "Artists do not exit")

    def delete(self):
        artist_id = request.args.get('artist_id')
        artist_id = artist_id if artist_id!=None else ""
        fetcher = Artists.query.filter_by(artist_id=artist_id).first()
        if fetcher:
            db.session.delete(fetcher)
            db.session.commit()
            return {f"Album Name : {artist_id} deleted"}, 200
        abort(400, message= "Artists do not exits")


api_ar.add_resource(artistTransaction, "/")
