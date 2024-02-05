from flask import make_response, jsonify, request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import Blueprint

#authentication_blueprint: Blueprint = Blueprint('authentication', __name__)


from app.models.diagnosis_model import Diagnosis, DiagnosisSchema
from app.models.patient_model import Patient
from app.models.user_model import Users
from app.patient.__init__ import patient_blueprint
from app.authentication import authentication_blueprint

class PatientDiagnosisView(MethodView):
    def __init__(self):
        self.diagnosis_schema = DiagnosisSchema(many=True)

    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        user = Users.get_user_by_id(identity)
        patient = Patient.get_by_user_id(user.user_id)
        try:
            diagnosis = Diagnosis.get_by_patient_id(patient_id=patient.patient_id)
            data = self.diagnosis_schema.dump(diagnosis)

            response = {
                'status': 'success',
                'data': data
            }
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {
                'status': 'error',
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

    @jwt_required
    def post(self):
        data = request.get_json()
        try:
            identity = get_jwt_identity()
            user = Users.get_user_by_id(identity)
            patient = Patient.get_by_user_id(user.user_id)
            diagnosis_uuid = Diagnosis.generate_slug()
            new_diagnosis = Diagnosis(
                diagnosis_uuid=diagnosis_uuid,
                diagnosis_name=data['diagnosis_name'],
                diagnosis_description=data['diagnosis_description'],
                diagnosis_image_url=data['diagnostic_image_url'],
                patient_id=patient.patient_id
            )
            new_diagnosis.save()
            health = Diagnosis.get_diagnosis(patient, Diagnosis.get_by_uuid(diagnosis_uuid=diagnosis_uuid),
                                             img=data['diagnosis_image_url'])
            response = {
                'status': 'success',
                'health': health
            }
            return make_response(jsonify(response)), 200
        except Exception as e:
            response = {
                'status': 'error',
                'message': str(e)
            }
            return make_response(jsonify(response)), 500

patient_diagonosis_view = PatientDiagnosisView.as_view('patient_diagnosis_view')

patient_blueprint.add_url_rule(
    '/patient/diagnosis',
    view_func=patient_diagonosis_view,
    methods=['POST']
)
