from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import logging

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

CORS(app, resources={
    r"/*": {
        "origins": [
            "https://hackathon-one-iota-59.vercel.app", # React Extrnal dev
            # "http://localhost:3000",  # React local dev
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
        "supports_credentials": True 
    }
})

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

# Setup console logging
if not app.debug:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)

# Create the database
with app.app_context():
    db.create_all()

app.logger.setLevel(logging.INFO)
app.logger.info('Flask App startup')