import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-default-secret-key')  
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
