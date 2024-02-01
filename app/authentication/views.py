from datetime import datetime

from flask import request, make_response, jsonify
from flask.views import MethodView

from app.authentication import authentication_blueprint
from app.models.failed_login_attempt_model import FailedLoginAttemptSchema, FailedLoginAttempt
from app.models.user_model import Users

NO_OF_ALLOWED_FAILED_LOGINS = 5


class UserAuthenticationSignUpView(MethodView):
    def post(self):
        audit_log_action = 'Authentication - Sign Up'
        try:
            data = request.get_json()
            user = Users.get_user_by_email(data['email'])
            if not user:
                user_uuid = Users.generate_slug()
                new_user = Users(
                    user_uuid=user_uuid,
                    forename=data['forename'],
                    lastname=data['lastname'],
                    email=data['email'],
                    password=data['password'],
                    phone_number=data['phone_number'],
                    is_verified=False
                )
                new_user.save()

                saved_user = Users.get_user_by_uuid(user_uuid)

                access_token = saved_user.generate_access_token(saved_user.user_id)

                # # Send email to verify account
                # verification_link = GenerateEmailVerificationLink(data['email'], access_token,
                #                                                   request.headers[
                #                                                       'Accept-Language']).email_verification_link()
                #
                # mail = SendEmail()
                # verification = mail.email_verification(data['email'], verification_link,
                #                                        request.headers['Accept-Language'])
                #
                # # Notify us on new sign up
                # # new_account_mail = {}
                # # if data['user_type'].lower() != 'job_seeker':
                # new_account_mail = mail.send_email_on_new_account_signup(data)

                response = {
                    'status': 'success',
                    'user_uuid': saved_user.user_uuid,
                    'account_activation_status': False,
                    'is_verified': False,
                    # 'new_account_mail': new_account_mail,
                    # 'vefication': verification,
                    'data': {'access_token': access_token}
                }
                return make_response(jsonify(response)), 201

            else:
                message = 'User with this email {} already exist'.format(data['email'])
                response = {
                    'status': 'fail',
                    'message': {'Error': message}
                }
                return make_response(jsonify(response)), 403
        except Exception as e:
            response = {
                'status': 'error',
                'message': str(e)
            }
            return make_response(jsonify(response)), 500


class UserAuthenticationLoginView(MethodView):
    def __init__(self):
        self.failed_login_attempts_schema = FailedLoginAttemptSchema(many=True)

    def post(self):
        audit_log_action = 'Authentication - Log in'
        try:
            data = request.get_json()
            # Check if user with same email exists
            user_data = Users.get_user_by_email(data['email'])
            # check if the limit is exceeded
            no_of_failed_attempts = FailedLoginAttempt.count_no_of_user_attempts(data['email'])
            remaining_attempts = NO_OF_ALLOWED_FAILED_LOGINS - no_of_failed_attempts
            if remaining_attempts >= 0:
                if user_data:
                    if user_data.password_is_valid(data['password']):
                        account_activation_status = False
                        is_onboarded = True
                        try:
                            access_token = user_data.generate_access_token(user_data.user_id)
                            last_login = user_data.last_login
                            response = {
                                "status": 'success',
                                'user_uuid': user_data.user_uuid,
                                'user_id': user_data.user_id,
                                'account_activation_status': account_activation_status,
                                'is_verified': user_data.is_verified,
                                'last_login': last_login,
                                'data': {'access_token': access_token}
                            }

                            # Update last login
                            user_data.last_login = str(datetime.now())
                            user_data.save()

                            # delete the failed logins
                            failed_attempts = FailedLoginAttempt.get_all_attempts(user_data.email)
                            failed_attempts.delete()

                            return make_response(jsonify(response)), 200

                        except Exception as e:
                            # An error occured, therefore return a string message containing the error
                            response = {
                                'status': 'error',
                                'message': str(e)
                            }

                            return make_response(jsonify(response)), 403
                    else:
                        message = 'Email or Password used is incorrect'
                        response = {
                            'status': 'fail',
                            'data': {'Error': message, 'remaining_attempts': remaining_attempts}
                        }
                        # record the failed login attempt
                        failed_login_attempt = FailedLoginAttempt(request.remote_addr, data['email'])
                        failed_login_attempt.save()
                        return make_response(jsonify(response)), 403
                else:
                    message = 'Email or Password used is incorrect'
                    response = {
                        'status': 'fail',
                        'data': {'Error': message, 'remaining_attempts': remaining_attempts}
                    }
                    # record the failed login attempt
                    failed_login_attempt = FailedLoginAttempt(request.remote_addr, data['email'])
                    failed_login_attempt.save()

                    return make_response(jsonify(response)), 403
            else:
                message = 'Number of Login attempts exceeded'
                response = {
                    'status': 'fail',
                    'data': {'Error': message, 'remaining_attempts': 0}
                }
                # record the failed login attempt
                failed_login_attempt = FailedLoginAttempt(request.remote_addr, data['email'])
                failed_login_attempt.save()

                return make_response(jsonify(response)), 429

        except Exception as e:
            response = {
                'status': 'error',
                'message': str(e)
            }
            return make_response(jsonify(response)), 500


user_auth_signup = UserAuthenticationSignUpView.as_view('user_auth_signup')
user_auth_login = UserAuthenticationLoginView.as_view('user_auth_login')

authentication_blueprint.add_url_rule(
    '/auth/signup',
    view_func=user_auth_signup,
    methods=['POST']
)

authentication_blueprint.add_url_rule(
    '/auth/signin',
    view_func=user_auth_login,
    methods=['POST']
)
