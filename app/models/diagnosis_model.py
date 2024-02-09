import random
import string
from datetime import datetime

import requests

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.preprocessing import image
from tensorflow.keras.losses import BinaryCrossentropy
from keras.optimizers import Adam
from PIL import Image

from app import db
from app.models.patient_model import Patient

from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Load the trained model with the correct input shape
# classification_model = load_model('algorithms/model-2.h5')

# print(model.summary())
# # Compile the model with the desired optimizer axnd loss function
# opt = Adam(learning_rate=0.01)
# model.compile(optimizer=opt, loss=BinaryCrossentropy(), metrics=['accuracy'])


# Define the model
# model = Sequential([
#     Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(224, 224, 3)),
#     MaxPooling2D(pool_size=(2, 2)),
#     Conv2D(64, kernel_size=(3, 3), activation='relu'),
#     MaxPooling2D(pool_size=(2, 2)),
#     Flatten(),
#     Dense(128, activation='relu'),
#     Dense(1, activation='sigmoid')
# ])

# # Compile the model
# model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Print the model summary to verify the input shape
# print(model.summary())

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

    @classmethod
    def get_diagnosis(cls, patient: Patient, diagnosis, img=None):
        try:
            if img:
                if isinstance(img, str):
                    # Send request with URL
                    result = cls.predict_from_url(img)
                else:
                    # Send request with image file
                    result = cls.predict_from_image(img)
            else:
                return {'error': 'No image data provided.'}
            
            diagnosis.diagnosis_description = result.get('class', 'No class found')
            patient.healthy = (result.get('class') != "infected")
            diagnosis.save()
            patient.save()
            
            return result
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def predict_from_url(img_url):
        prediction_url = "https://pcosdetection-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/d91467d5-51e8-47df-94ff-93276d9ab469/detect/iterations/Iteration6/url"
        prediction_key = "6b734e4ac84c48ea842724c183715985"
        headers = {
            "Prediction-Key": prediction_key,
            "Content-Type": "application/json"
        }
        data = {
            "Url": img_url
        }
        response = requests.post(prediction_url, headers=headers, json=data)
        return response.json()
    
    @staticmethod
    def predict_from_image(img_file):
        prediction_url = "https://pcosdetection-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/d91467d5-51e8-47df-94ff-93276d9ab469/detect/iterations/Iteration6/image"
        prediction_key = "6b734e4ac84c48ea842724c183715985"
        headers = {
            "Prediction-Key": prediction_key,
            "Content-Type": "application/octet-stream"
        }
        with open(img_file, "rb") as file:
            img_data = file.read()
        response = requests.post(prediction_url, headers=headers, data=img_data)
        return response.json()


    # Load the image from the URL and preprocess it
    # def preprocess_image(img_url):
    #     try:
    #         # Load the image
    #         img = Image.open(requests.get(img_url, stream=True).raw)
    #         # Resize the image to (224, 224) and convert it to an array
    #         img_array = np.array(img.resize((224, 224)))
    #         # Ensure that the image array has shape (224, 224, 3)
    #         if img_array.shape[-1] != 3:
    #             raise ValueError("Invalid number of channels. Expected 3 channels (RGB).")
    #         return img_array
    #     except Exception as e:
    #         raise ValueError(f"Failed to preprocess image: {str(e)}")

class DiagnosisSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Diagnosis
        include_relationships = True
        load_instance = True
