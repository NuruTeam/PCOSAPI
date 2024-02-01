import random
import string
from datetime import datetime
from app import db, ma
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class FailedLoginAttempt(db.Model):
    __tablename__ = 'failed_login_attempts'

    log_id = db.Column(db.Integer, primary_key=True)
    log_uuid = db.Column(db.String(256), index=True)
    ip_address = db.Column(db.String(256))
    email = db.Column(db.String(256))
    created_at = db.Column(db.DateTime)

    # FailedLoginAttempt initialization
    def __init__(self, ip_address, email):
        self.log_uuid = FailedLoginAttempt.generate_slug()
        self.ip_address = ip_address
        self.created_at = datetime.now()
        self.email = email
        self.ip_address = ip_address

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return FailedLoginAttempt.query.all()

    @staticmethod
    def count_no_of_user_attempts(email):
        return FailedLoginAttempt.query.filter_by(email=email).count()

    @staticmethod
    def get_all_attempts(email):
        return FailedLoginAttempt.query.filter_by(email=email)

    @staticmethod
    def generate_slug():
        letters = string.ascii_letters
        slug = 'FLA' + ''.join(random.choice(letters) for i in range(16))
        return slug


class FailedLoginAttemptSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = FailedLoginAttempt
        include_relationships = True
        load_instance = True

