from flask import Blueprint, jsonify
from flask_restful import Api, Resource, marshal_with, reqparse, fields, abort
from app.models import db, Users

api_user = Blueprint("api_u",__name__)
api_u = Api(api_user)

returner = {
    "user_id":fields.Integer,
    "user_name":fields.String,
    "user_password":fields.String,
    "creator_id":fields.Integer,
    "playlists":fields.String
}

user_post = reqparse.RequestParser()
user_post.add_argument("user_name", type=str, help="Enter user name",required=True)
user_post.add_argument("user_password", type=str, help="Enter user password",required=True)
user_post.add_argument("creator_id", type=int, help="Enter creator id")
user_post.add_argument("playlists", type=str, help="Enter playlist")

user_put = reqparse.RequestParser()
user_put.add_argument("creator_id", type=int, help="Enter creator id")
user_put.add_argument("playlists", type=str, help="Enter playlist")
class userTransaction(Resource):
    @marshal_with(returner)
    def get(self,user_id):
        data = Users.query.filter_by(user_id=user_id).first()
        if data:
            return data, 200
        abort(400,message="User do not exist")

    @marshal_with(returner)
    def get(self,user_name,user_password):
        data = Users.query.filter_by(user_name=user_name,user_password=user_password).first()
        if data:
            return data, 200
        abort(400,message="User do not exist")
    
    @marshal_with(returner)
    def post(self):
        req = user_post.parse_args()
        fetcher = Users.query.filter_by(user_name=req["user_name"]).first()
        if (fetcher==None):
            userEntry = Users(
                user_name = req["user_name"],
                user_password = req["user_password"],
                creator_id =  req["creator_id"] if req["creator_id"] else None,
                playlists = req["playlists"] if req["playlists"] else None,
            )
            db.session.add(userEntry)
            db.session.commit()
            fetcher = Users.query.filter_by(user_name=req["user_name"]).first()
            return fetcher, 200
        abort(400,message="User Name exists.")

    @marshal_with(returner)
    def put(self,user_id):
        req = user_put.parse_args()
        fetcher = Users.query.filter_by(user_id=user_id).first()
        if req["creator_id"]:
            fetcher.creator_id = req["creator_id"]
        elif req["playlists"]:
            fetcher.playlists = req["playlists"]
        db.session.commit()
        return fetcher, 200
    
api_u.add_resource(userTransaction,"/<int:user_id>","/","/<user_name>/<user_password>")