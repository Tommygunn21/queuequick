import os

# Get the database URL from the environment variable
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///queuequick.db')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False


