import os

from flask import Flask
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig'
)

app.config.from_object(app_settings)

db = MongoEngine(app)
bcrypt = Bcrypt(app)

from app import routes
