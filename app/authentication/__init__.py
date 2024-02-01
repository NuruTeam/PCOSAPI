from flask import Blueprint

authentication_blueprint = Blueprint('authentication_blueprint', __name__)

from . import views
