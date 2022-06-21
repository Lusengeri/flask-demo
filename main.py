import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from api.config import config
from api.routes.users import user_routes
from api.utils.api import ma 
from api.utils.database import db
from api.utils.email import mail
from api.utils.observe import metrics 
from api.utils.responses import response_with 
import api.utils.responses as resp 

def create_app(user_config=None):
    app = Flask(__name__)

    if not (user_config == None):
        app.config.from_object(user_config)
    else:
        if os.environ.get('WORK_ENV') == 'production': 
            app_config = config.ProductionConfig
        elif os.environ.get('WORK_ENV') == 'testing':
            app_config = config.TestingConfig
        else:
            app_config = config.DevelopmentConfig

        app.config.from_object(app_config)

    @app.route('/hello')
    def hello_world():
        return "Hello, Flask World!"

    app.register_blueprint(user_routes, url_prefix='/api/users')

    # Initialize Flask extensions

    db.init_app(app)

    with app.app_context():
        db.create_all()

    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    ma.init_app(app)
    mail.init_app(app)

    
    metrics.init_app(app)

    # static information as metric
    metrics.info('app_info', 'Application info', version='1.0.3')
    
    return app

def clear_app_db(app):
    with app.app_context():
        db.close_all_sessions()
        db.drop_all()

app = create_app()
