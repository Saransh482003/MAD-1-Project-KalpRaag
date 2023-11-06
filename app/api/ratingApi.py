from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, marshal_with, reqparse, fields, abort
from app.models import db, Rating

api_rating = Blueprint("api_r", __name__)
api_r = Api(api_rating)

returner = {
    "s_no": fields.Integer,
    "song_id": fields.Integer,
    "rating": fields.Integer,
    "love": fields.Integer,
    "user_name": fields.String,
}

rating_post = reqparse.RequestParser()
rating_post.add_argument("song_id", type=int,help="Enter associated song id", required=True)
rating_post.add_argument("rating", type=int,help="Enter rating", required=True)
rating_post.add_argument("love", type=int,help="Enter love", required=True)
rating_post.add_argument("user_name", type=str,help="Enter user name", required=True)

rating_put = reqparse.RequestParser()
rating_put.add_argument("song_id", type=int,help="Enter associated song id")
rating_put.add_argument("rating", type=int,help="Enter rating")
rating_put.add_argument("love", type=int,help="Enter love")
rating_put.add_argument("user_name", type=str,help="Enter user name")


class ratingTransaction(Resource):
    @marshal_with(returner)
    def get(self):
        s_no = request.args.get('s_no')
        song_id = request.args.get('song_id')
        rating = request.args.get('rating')
        love = request.args.get('love')
        user = request.args.get('user_name')

        if song_id and user:
            data = Rating.query.filter_by(song_id=song_id, user_name=user).first()
        else:
            if s_no:
                data = Rating.query.filter_by(s_no=s_no).first()
            elif song_id:
                data = Rating.query.filter_by(song_id=song_id).all()
            elif rating:
                data = Rating.query.filter_by(rating=rating).all()
            elif love:
                data = Rating.query.filter_by(love=love).all()
            elif user:
                data = Rating.query.filter_by(user_name=user).all()
            else:
                data = Rating.query.all()

        if data:
            return data, 200
        abort(400, message="Rating does not exist")


    @marshal_with(returner)
    def post(self):
        req = rating_post.parse_args()
        fetcher = Rating.query.filter_by(song_id=req["song_id"],user_name=req["user_name"]).first()
        if (fetcher == None):
            ratingEntry = Rating(
                song_id=req["song_id"],
                rating=req["rating"],
                love=req["love"],
                user_name=req["user_name"],
            )
            db.session.add(ratingEntry)
            db.session.commit()
            fetcher = Rating.query.filter_by(song_id=req["song_id"],user_name=req["user_name"]).first()
            return fetcher, 200
        abort(400, message="Rating Name exists.")

    @marshal_with(returner)
    def put(self):
        # s_no = request.args.get('s_no')
        # s_no = s_no if s_no!=None else ""
        req = rating_put.parse_args()
        fetcher = Rating.query.filter_by(song_id=req["song_id"],user_name=req["user_name"]).first()
        if fetcher:
            for i in req:
                setattr(fetcher,i,req[i])
            db.session.commit()
            fetcher = Rating.query.filter_by(song_id=req["song_id"],user_name=req["user_name"]).first()
            return fetcher, 200
        abort(400, message="Rating do not exit")

    def delete(self):
        song_id = request.args.get('song_id')
        song_id = song_id if song_id!=None else ""
        fetcher = Rating.query.filter_by(song_id=song_id)
        if fetcher:
            for i in fetcher:
                db.session.delete(i)
            db.session.commit()
            return {f"Song ID : {song_id} deleted"}, 200
        abort(400, message="Rating do not exits")


api_r.add_resource(ratingTransaction, "/")
