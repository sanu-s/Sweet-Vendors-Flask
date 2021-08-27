import argparse

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


# Initialize parser
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--settings', help='Settings Name', required=True)

# Read arguments from command line
args = parser.parse_args()

if args.settings == 'development':
    from app.settings import DevelopmentSettings as Settings
elif args.settings == 'staging':
    from app.settings import StagingSettings as Settings
elif args.settings == 'production':
    from app.settings import ProductionSettings as Settings
else:
    raise SystemExit(
        "Invalid settings name.\nProvide any one of the settings [development/staging/production].")


# Setup Flask Configurations
app = Flask(__name__)
app.config.from_object(Settings)
db = SQLAlchemy(app)
jwt = JWTManager(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
