import os
import devtools

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:190407011@localhost:5432/blogApp'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "developer"
    SECURITY_PASSWORD_SALT = "sdjfjds"
    security_password_hash = "djfsfhj"