from flask import Flask
from config.database import DBConfig
from config.jwt import JWTConfig
from app.extension import db, jwt
from flask_migrate import Migrate
from config.logging import file_handler

def create_app():
    app = Flask(__name__)

    # Register file-based logger
    app.logger.addHandler(file_handler)

    # Database & JWT config
    app.config.from_object(DBConfig)
    app.config.from_object(JWTConfig)

    db.init_app(app)
    jwt.init_app(app)
    # Initialize database migration
    Migrate(app, db)

    @app.route('/')
    def index():
        return 'Hello, World!'

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)