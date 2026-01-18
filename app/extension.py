from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# SQLAlchemy & JWT instance
db = SQLAlchemy()
jwt = JWTManager()