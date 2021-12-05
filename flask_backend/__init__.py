#coding=utf-8
import os
from flask import Flask
from flask.helpers import url_for
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_login import LoginManager, login_manager
from flask_socketio import SocketIO
from flask_cors import CORS

from datetime import timedelta

socketio = SocketIO()

pymysql.install_as_MySQLdb()
db = SQLAlchemy()
jwt = JWTManager()



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'JustDemonstrating'
    app.config['JWT_SECRET_KEY'] = 'this-should-be-change'


    ####### token ###########
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=1)#1
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(minutes=20)#20
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]


    ######## Register Database ########
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:joyce50635@127.0.0.1:3306/flask'
    #app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)



    jwt.init_app(app)
    migrate = Migrate(app, db)
    db.create_all(app=app)
    CORS(app, supports_credentials=True, origins = ['http://localhost:3000'])

    ######## Register websocket ########
    socketio.init_app(app, async_mode=None, cors_allowed_origins='*')


    ### 建立view
    from .views import views
    from .auth import auth
    from .user import user
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(user, url_prefix="/user")

    ### 建立login_manager
    from .models import User
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app, socketio

