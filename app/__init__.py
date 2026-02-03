
from app.commands.seed import seed_command
from config.mail import MailConfig
from flask import Flask
from flask_cors import CORS
from config.cors import CORS_CONFIG
from config.database import DBConfig
from config.jwt import JWTConfig
from app.extension import db, jwt, mail
from flask_migrate import Migrate
from routes.api import api
from routes.auth import auth
from config.logging import file_handler

app = Flask(__name__)

# CORS config
CORS(app, **CORS_CONFIG)

# Register file-based logger
app.logger.addHandler(file_handler)

# Database, JWT & Mail config
app.config.from_object(DBConfig)
app.config.from_object(JWTConfig)
app.config.from_object(MailConfig)

db.init_app(app)
jwt.init_app(app)
mail.init_app(app)
# Initialize database migration
Migrate(app, db)

# models intialize
from app.models import *

# Register blueprints
app.register_blueprint(auth, url_prefix = '/auth')
app.register_blueprint(api, url_prefix = '/api')

# register flask command
app.cli.add_command(seed_command)

if __name__ == '__main__':
    app.run(debug=True)