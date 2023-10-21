from flask import Flask
from .models import db
from .api.userApi import api_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kalpRaag.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

db.init_app(app)

app.register_blueprint(api_bp, url_prefix="/api")