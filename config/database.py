import os
from dotenv import load_dotenv

load_dotenv()

# MySQL connection parameters
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "user_management")

class DBConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    # Disable SQLAlchemy event notifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False