import os
import base64

class Config:
    SECRET_KEY = base64.b64decode(os.getenv('SECRET_KEY')).decode('utf-8')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')