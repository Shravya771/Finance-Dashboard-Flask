import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey1234567890")
    SQLALCHEMY_DATABASE_URI = "sqlite:///finance.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key-1234567890")
