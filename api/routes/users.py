from flask import Blueprint, request, url_for, render_template_string

from flask_jwt_extended import create_access_token

from api.models.users import User, UserSchema

from api.utils import responses as resp
from api.utils.database import db
from api.utils.email import send_email 
from api.utils.responses import response_with
from api.utils.token import generate_verification_token, confirm_verification_token

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    print(data)
    print(type(data))

    if 'email' not in data or 'username' not in data or 'password' not in data:
        return response_with(resp.INVALID_INPUT_422)

    if (User.find_by_email(data['email']) is not None or User.find_by_username(data['username']) is not None):
        return response_with(resp.INVALID_INPUT_422)

    try:
        data['password'] = User.generate_hash(data['password'])
        user_schema = UserSchema()
        user = user_schema.load(data)
        result = user_schema.dump(user.create())
    except Exception as e:
        print("exception:", e)
        return response_with(resp.BAD_REQUEST_400)

    return response_with(resp.SUCCESS_201, value={'user': result})

    # try:
    #     data['password'] = User.generate_hash(data['password'])
    #     user_schema = UserSchema()
    #     user = user_schema.load(data)
    #     token = generate_verification_token(data['email'])
    #     verification_email = url_for('user_routes.verify_email', token=token, _external=True)
    #     html = render_template_string("<p>Welcome! Thanks for signing up. Please follow this link to activate your account:<p> <p><a href='{{verification_email}}'>{{verification_email}}</a></p> <br> <p>Thanks!</p>", verification_email=verification_email)
    #     subject = "Please verify your email"
    #     send_email(user.email, subject, html)
    #     result = user_schema.dump(user.create())
    #     return response_with(resp.SUCCESS_201)
    # except Exception as e:
    #     print(e)
    #     return response_with(resp.INVALID_INPUT_422)

#@user_routes.route('/confirm/<token>', methods=['GET'])
#def verify_email(token):
#    try:
#        email = confirm_verification_token(token)
#    except:
#        return response_with(resp.SERVER_ERROR_401)
#
#    user = User.query.filter_by(email=email).first_or_404()
#
#    if user.isVerified:
#        return response_with(resp.INVALID_INPUT_422)
#    else:
#        user.isVerified = True
#        db.session.add(user)
#        db.session.commit()
#        return response_with(resp.SUCCESS_200, value={'message': 'E-mail verified, you can proceed to login now.'})

@user_routes.route('/login', methods=['POST'])
def authenticate_user():
    try:
        data = request.get_json()
        print(data)
        current_user = None

        if 'username' in data:
            current_user = User.find_by_username(data['username'])
        elif 'email' in data:
            current_user = User.find_by_email(data['email'])
        else:
            return response_with(resp.INVALID_INPUT_422)

#        if current_user and not current_user.isVerified:
#            return response_with(resp.BAD_REQUEST_400)

        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity = current_user.email)
            return response_with(resp.SUCCESS_200, value={'message': 'Logged in as {}'.format(current_user.username), "access_token": access_token})
        else:
            return response_with(resp.UNAUTHORIZED_401)
    except Exception as e:
        print("exception:", e)
        return response_with(resp.INVALID_INPUT_422)
