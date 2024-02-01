from flask import Blueprint

patient_blueprint = Blueprint('patient_blueprint', __name__)

from . import views
