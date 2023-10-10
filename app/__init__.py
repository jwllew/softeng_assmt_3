from flask import Flask, request
from flask_login import LoginManager
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))   

db = SQLAlchemy()
moment = Moment()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    #Configs
    app.config.update(dict(
        SECRET_KEY = '70538c79-4b88-4da3-8196-85eb0ff45e5d',
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
    ))


    db.init_app(app)
    moment.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
   
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

