import os

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test_db"
    SQLALCHEMY_ECHO = False

    JWT_SECRET_KEY="b'\x99\xceK\x0ev\x9b\xb6\xf7q\x89`\x92\xcf]"
    SECRET_KEY = 'my_secured_key_here'
    SECURITY_PASSWORD_SALT = 'my_security_password_here'

    MAIL_DEFAULT_SENDER = 'admin@gmail.com'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'admin@gmail.com'
    MAIL_PASSWORD = 'terroriste101*'
    MAIL_USE_TLS = False 
    MAIL_USE_SSL = True 
