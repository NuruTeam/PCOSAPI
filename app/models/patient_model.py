import random
import string
from datetime import datetime

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app import db


class Patient(db.Model):
    __tablename__ = 'patients'

    patient_id = db.Column(db.Integer, primary_key=True)
    patient_uuid = db.Column(db.String(256))
    age = db.Column(db.Integer)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    gender = db.Column(db.String(256))
    healthy = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), index=True)

    def __init__(self, patient_uuid, age, height, weight, gender, user_id):
        self.patient_uuid = patient_uuid
        self.age = age
        self.height = height
        self.weight = weight
        self.gender = gender
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def generate_slug(cls):
        letters = string.ascii_letters
        slug = 'PA' + ''.join(random.choices(letters, k=13))
        return slug

    @classmethod
    def get_by_id(cls, patient_id):
        return cls.query.filter_by(patient_id=patient_id).first()

    @classmethod
    def get_by_uuid(cls, patient_uuid):
        return cls.query.filter_by(patient_uuid=patient_uuid).first()

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()


class PatientSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Patient
        include_relationships = True
        load_instance = True
