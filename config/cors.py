# config/cors.py

CORS_CONFIG = {
    "origins": ["http://localhost:5173", "http://localhost:3000"],
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "allow_headers": ["Content-Type", "Authorization", "skipAuth", "X-CSRF-TOKEN"],
    "supports_credentials": True,
}
