import random
import string
from datetime import timedelta

from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

from app import db


class Users(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(db.String(256))
    forename = db.Column(db.String(256))
    lastname = db.Column(db.String(256))
    email = db.Column(db.String(256))
    password = db.Column(db.String(256))
    phone_number = db.Column(db.String(256))
    is_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime)

    def __init__(self, forename, lastname, user_uuid, email, phone_number, is_verified,
                 password=None):
        self.forename = forename
        self.lastname = lastname
        self.user_uuid = user_uuid
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.phone_number = phone_number
        self.is_verified = is_verified

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def generate_password_hash(cls, password):
        return Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        if not self.password:
            return False
        return Bcrypt().check_password_hash(self.password, password)

    @classmethod
    def update_password(cls, new_password):
        updated_password = Bcrypt().generate_password_hash(new_password).decode()
        return updated_password

    @classmethod
    def generate_access_token(cls, user_id):
        """"Generate the access Token"""
        try:
            expires = timedelta(days=1)
            user_data = Users.query.filter_by(user_id=user_id).first()
            access_token = create_access_token(
                identity=user_id,
                expires_delta=expires,
                additional_claims={'user_uuid': user_data.user_uuid}
            )

            return access_token

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @classmethod
    def generate_slug(cls):
        letters = string.ascii_letters
        slug = 'US' + ''.join(random.choice(letters) for i in range(16))
        return slug

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_user_by_uuid(cls, user_uuid):
        return cls.query.filter_by(user_uuid=user_uuid).first()

    @classmethod
    def get_user_by_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()
