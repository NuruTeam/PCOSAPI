import random
import string
from datetime import datetime

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.losses import BinaryCrossentropy
from keras.optimizers import Adam


from app import db
from app.models.patient_model import Patient

# Load the trained model with the correct input shape
# classification_model = load_model('algorithms/model-2.h5')

# print(model.summary())
# Compile the model with the desired optimizer and loss function
# opt = Adam(learning_rate=0.01)
# model.compile(optimizer=opt, loss=BinaryCrossentropy(), metrics=['accuracy'])


# Define the classes
classes = ['infected', 'notinfected']


class Diagnosis(db.Model):
    __tablename__ = 'diagnosis'

    diagnosis_id = db.Column(db.Integer, primary_key=True)
    diagnosis_uuid = db.Column(db.String(36), unique=True, nullable=False)
    diagnosis_name = db.Column(db.String())
    diagnosis_description = db.Column(db.String())
    diagnosis_date_created = db.Column(db.DateTime, default=datetime.utcnow)
    diagnosis_image_url = db.Column(db.String())
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'))

    def __init__(self, diagnosis_uuid, diagnosis_name, diagnosis_description, diagnosis_image_url, patient_id):
        self.diagnosis_uuid = diagnosis_uuid
        self.diagnosis_name = diagnosis_name
        self.diagnosis_description = diagnosis_description
        self.diagnosis_image_url = diagnosis_image_url
        self.patient_id = patient_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def generate_slug(cls):
        letters = string.ascii_letters
        slug = 'DI' + ''.join(random.choices(letters, k=13))
        return slug

    @classmethod
    def get_by_id(cls, diagnosis_id):
        return cls.query.filter_by(diagnosis_id=diagnosis_id).first()

    @classmethod
    def get_by_uuid(cls, diagnosis_uuid):
        return cls.query.filter_by(diagnosis_uuid=diagnosis_uuid).first()

    @classmethod
    def get_by_patient_id(cls, patient_id):
        return cls.query.filter_by(patient_id=patient_id)

    # @classmethod
    # def get_diagnosis(cls, patient: Patient, diagnosis, img):
    #     try:
    #         # Preprocess the image
    #         img_array = image.img_to_array(img)
    #         # Assuming your model expects images with shape (224, 224, 3)
    #         img_array = tf.image.resize(img_array, (224, 224))
    #         img_array = np.expand_dims(img_array, axis=0)
    #         img_array /= 255.0  # Normalize the image
    #
    #
    #
    #         # Make predictions
    #         predictions = model.predict(img_array)
    #
    #         # Get the predicted class
    #         predicted_class = classes[np.argmax(predictions)]
    #
    #         # Return the prediction result
    #         result = {'class': predicted_class, 'confidence': float(predictions[0][np.argmax(predictions)])}
    #         diagnosis.diagnosis_description = result
    #         if result == "infected":
    #             patient.healthy = False
    #         else:
    #             patient.healthy = False
    #         diagnosis.save()
    #         patient.save()
    #         return result
    #
    #     except Exception as e:
    #         return {'error': str(e)}


class DiagnosisSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Diagnosis
        include_relationships = True
        load_instance = True
