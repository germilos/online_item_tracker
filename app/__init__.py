from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'onlineitemtracker',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine(app)

from app import routes
