# PCOS Image Detection Flask API

Welcome to the PCOS Image Detection Flask API! This API is designed to perform PCOS image detection, determining whether an image is infected or not. The application uses a SQL database hosted on Azure SQL to store user and diagnosis information. Follow the instructions below to set up and run the API.

## Prerequisites

- Python 3.x
- Flask
- Flask-JWT-Extended
- Azure SQL Database

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/pcos-image-detection-api.git
   cd pcos-image-detection-api
2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

# Configuration

1. Create a `.env` file based on the provided `.env.example` file.

2. Update the `.env` file with your Azure SQL Database connection details and other necessary configuration.

# Database Migration

To perform database migration, run the following commands:

```bash
flask db migrate
flask db upgrade
```

# Running the Application

To run the application, execute the following command:

```bash
flask run -p 6001
```

or

```bash
python run.py
```

# API Endpoints

## Patient Diagnosis

### `GET /patient/diagnosis`

- **Description:** Retrieve diagnosis information for the authenticated patient.
- **Authorization:** JWT Token required.
- **Response:**
  - `200 OK` on success with diagnosis information.
  - `500 Internal Server Error` on failure.

### `POST /patient/diagnosis`

- **Description:** Submit a new diagnosis for the authenticated patient.
- **Authorization:** JWT Token required.
- **Request Body:**
  - `diagnosis_name`: Name of the diagnosis.
  - `diagnosis_description`: Description of the diagnosis.
  - `diagnosis_image_url`: URL of the diagnostic image.
- **Response:**
  - `201 Created` on success with the new diagnosis information.
  - `500 Internal Server Error` on failure.

## Authentication

### `POST /auth/signup`

- **Description:** Sign up a new user.
- **Request Body:**
  - `forename`: User's first name.
  - `lastname`: User's last name.
  - `email`: User's email address.
  - `password`: User's password.
  - `phone_number`: User's phone number.
- **Response:**
  - `201 Created` on success with user information and access token.
  - `403 Forbidden` if the user already exists.
  - `500 Internal Server Error` on failure.

### `POST /auth/signin`

- **Description:** Log in a user.
- **Request Body:**
  - `email`: User's email address.
  - `password`: User's password.
- **Response:**
  - `200 OK` on success with user information and access token.
  - `403 Forbidden` if the login credentials are incorrect.
  - `429 Too Many Requests` if the number of login attempts exceeds the limit.
  - `500 Internal Server Error` on failure.

# Models

All database models are defined in the `models` folder in the `app` directory.

Feel free to explore and modify the code to suit your specific requirements. If you have any questions or issues, please don't hesitate to reach out!

