from flask import Blueprint, jsonify
from flask_restful import Api, Resource, marshal_with, reqparse, fields, abort, request
from app.models import db, Admin

api_admin = Blueprint("api_ad",__name__)
api_ad = Api(api_admin)

returner = {
    "admin_id":fields.Integer,
    "user_name":fields.String,
    "password":fields.String,
    "blacklist":fields.String,
    "whitelist":fields.String
}

admin_post = reqparse.RequestParser()
admin_post.add_argument("user_name", type=str, help="Enter user name",required=True)
admin_post.add_argument("password", type=str, help="Enter user password",required=True)
admin_post.add_argument("blacklist", type=str, help="Enter blacklist",required=True)
admin_post.add_argument("whitelist", type=str, help="Enter whitelist",required=True)

admin_put = reqparse.RequestParser()
admin_put.add_argument("user_name", type=str, help="Enter user name")
admin_put.add_argument("password", type=str, help="Enter user password")
admin_put.add_argument("blacklist", type=str, help="Enter blacklist")
admin_put.add_argument("whitelist", type=str, help="Enter whitelist")
class adminTransaction(Resource):
    @marshal_with(returner)
    def get(self):
        admin_id = request.args.get('admin_id')
        user_name = request.args.get('user_name')
        password = request.args.get('password')
        blacklist = request.args.get('blacklist')
        whitelist = request.args.get('whitelist')
        
        if user_name and password:
            data = Admin.query.filter_by(user_name=user_name,password=password).first()
        else:
            if admin_id:
                data = Admin.query.filter_by(admin_id=admin_id).first()
            elif user_name:
                data = Admin.query.filter_by(user_name=user_name).first()
            elif password:
                data = Admin.query.filter_by(password=password).first()
            elif blacklist:
                data = Admin.query.filter_by(blacklist=blacklist).first()
            elif whitelist:
                data = Admin.query.filter_by(whitelist=whitelist).all()
            else:
                data = Admin.query.all()

        if data:
            return data, 200
        abort(400, message= "Admin does not exist")
    
    @marshal_with(returner)
    def post(self):
        req = admin_post.parse_args()
        fetcher = Admin.query.filter_by(user_name=req["user_name"]).first()
        if (fetcher==None):
            adminEntry = Admin(
                user_name = req["user_name"],
                password = req["password"],
                blacklist =  req["blacklist"] if req["blacklist"] else None,
                whitelist = req["whitelist"] if req["whitelist"] else None,
            )
            db.session.add(adminEntry)
            db.session.commit()
            fetcher = Admin.query.filter_by(user_name=req["user_name"]).first()
            return fetcher, 200
        abort(400,message="User Name exists.")

    @marshal_with(returner)
    def put(self):
        req = admin_put.parse_args()
        user_name = request.args.get("user_name")
        fetcher = Admin.query.filter_by(user_name=user_name).first()
        if req["creator_id"]:
            fetcher.creator_id = req["creator_id"]
        # elif req["playlists"]:
        #     fetcher.playlists = req["playlists"]
        db.session.commit()
        return fetcher, 200
    

    
api_ad.add_resource(adminTransaction,"/<int:user_id>","/","/<user_name>/<user_password>")