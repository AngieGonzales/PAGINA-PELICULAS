import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/peliculas'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.urandom(24)
    UPLOAD_FOLDER = 'app/static/uploads'  
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
