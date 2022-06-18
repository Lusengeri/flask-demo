import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from api.routes.users import user_routes
from api.config import config
from api.utils.api import ma 
from api.utils.email import mail
from api.utils.database import db
from api.utils.responses import response_with 
import api.utils.responses as resp 

app = Flask(__name__)

# Application configuration
if os.environ.get('WORK_ENV') == 'production': 
    app_config = config.ProductionConfig
elif os.environ.get('WORK_ENV') == 'testing':
    app_config = config.TestingConfig
else:
    app_config = config.DevelopmentConfig

app.config.from_object(app_config)

app.register_blueprint(user_routes, url_prefix='/api/users')

# Flask extensions
db.init_app(app)

with app.app_context():
    db.create_all()

jwt = JWTManager(app)
migrate = Migrate(app, db)
ma.init_app(app)
mail.init_app(app)

@app.route('/')
def hello_world():
    return "Hello, Flask World!"
