import json
import tempfile
import pytest
import random
import string
from datetime import datetime

from main import create_app
from api.utils.token import generate_verification_token, confirm_verification_token

from api.models.users import User

def random_string_generator():
    return ''.join(random.choice(string.ascii_letters) for x in range(12))

def create_test_users():
    user1 = User(email='lusengeri@gmail.com', username='lusengeri', password=User.generate_hash('password1'), isVerified=True).create()
    user2 = User(email='jdhobiz@gmail.com', username='johnny', password=User.generate_hash('password2')).create()

def test_create_user_returns_correct_response_on_success(client):
    test_username = random_string_generator()
    test_password = random_string_generator()
    test_email = random_string_generator()

    user = {"username": test_username, "password": test_password, "email": test_email}

    response = client.post('/api/users/', data=json.dumps(user), content_type='application/json')
    data = json.loads(response.data)

    assert response.status_code == 201
    assert('user' in data, 'username' in data['user'] and 'email' in data['user'])
    assert(data['user']['username'] == test_username and data['user']['email'] == test_email)

def test_create_user_fails_if_already_exists(app, client):
    create_test_users()
    user = {"username": "lusengeri", "password": "password1", "email": "lusengeri@gmail.com"}
    response = client.post('/api/users/', data=json.dumps(user), content_type='application/json')
    assert response.status_code == 422 

def test_create_user_fails_on_incomplete_input(client):
    user = {"password": "password1", "email": "lusengeri@gmail.com"}
    response = client.post('/api/users/', data=json.dumps(user), content_type='application/json')
    assert response.status_code == 422 

def test_login_user_succeeds_on_valid_email(client):
    create_test_users()
    user = {'email': 'jdhobiz@gmail.com', 'password': 'password2'}
    response = client.post('/api/users/login', data=json.dumps(user), content_type='application/json')
    data = json.loads(response.data)
    assert(response.status_code == 200)
    assert('access_token' in data)

def test_login_user_succeeds_on_valid_username(client):
    create_test_users()
    user = {'username': 'johnny', 'password': 'password2'}
    response = client.post('/api/users/login', data=json.dumps(user), content_type='application/json')
    data = json.loads(response.data)
    assert(response.status_code == 200)
    assert('access_token' in data)

def test_login_user_fails_on_incorrect_password(client):
    create_test_users()
    user = {'email': 'jdhobiz@gmail.com', 'password': 'incorrect-password'}
    response = client.post('/api/users/login', data=json.dumps(user), content_type='application/json')
    data = json.loads(response.data)
    assert(response.status_code == 401)
    assert("Wrong email password combination" in data.values())

def test_login_user_fails_on_invalid_credentials(client):
    create_test_users()
    user = {'email': 'fake_user@fakedomain', 'password': 'fake_password'}
    response = client.post('/api/users/login', data=json.dumps(user), content_type='application/json')
    assert(response.status_code == 422)

    #def test_login_user(self):
    #    user = {"email": "kunal.relan12@gmail.com", "password": "helloworld"}
    #    response = self.app.post('/api/users/login', data=json.dumps(user), content_type='application/json')
    #    data = json.loads(response.data)
    #    self.assertEqual(200, response.status_code)
    #    self.assertTrue('access_token' in data)

    #def test_login_user_wrong_credentials(self):
    #    user = {"email": "kunal.relan12@gmail.com", "password": "helloworld12"}
    #    response = self.app.post('/api/users/login', data=json.dumps(user), content_type='application/json')
    #    data = json.loads(response.data)
    #    self.assertEqual(401, response.status_code)

    #def test_login_unverified_user(self):
    #    user = {"email": "kunal.relan123@gmail.com", "password": "helloworld"}
    #    response = self.app.post('/api/users/login', data=json.dumps(user), content_type='application/json')
    #    data = json.loads(response.data)
    #    self.assertEqual(400, response.status_code)
    
    #def test_confirm_email(self):
    #    token = generate_verification_token('kunal.relan123@gmail.com')
    #    response = self.app.get('/api/users/confirm/' + token)
    #    data = json.loads(response.data)
    #    self.assertEqual(200, response.status_code)
    #    self.assertTrue('success' in data['code'])

    #def test_confirm_email_with_incorrect_email(self):
    #    token = generate_verification_token('jdhobiz@gmail.com')
    #    response = self.app.get('/api/users/confirm/'+token)
    #    data = json.loads(response.data)
    #    self.assertEqual(404, response.status_code)

    #def test_confirm_email_for_verified_user(self):
    #    token = generate_verification_token('kunal.relan12@gmail.com')
    #    response = self.app.get('/api/users/confirm/'+token)
    #    data = json.loads(response.data)
    #    self.assertEqual(422, response.status_code)
