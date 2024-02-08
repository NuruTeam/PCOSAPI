import os

from flask_api import FlaskAPI
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

app = FlaskAPI(__name__, instance_relative_config=True)
ma = Marshmallow(app)
CORS(app)
migrate = Migrate(app, db)


def create_app(config_name):
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'dffbjkjfjnsfjfamf_nefjkhe'
    app.secret_key = os.environ.get('SECRET')
    db.init_app(app)
    jwt = JWTManager(app)

    from app.authentication import authentication_blueprint
    from app.patient import patient_blueprint

    app.register_blueprint(authentication_blueprint)
    app.register_blueprint(patient_blueprint)
    
    print("Patient blueprint registered successfully.") 

    return app