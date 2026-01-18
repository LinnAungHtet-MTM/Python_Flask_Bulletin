import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class JWTConfig:

    # JWT connection parameters
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 30)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 7)))