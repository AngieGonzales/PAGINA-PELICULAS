from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config.from_object('config.Config')

    db.init_app(app)

    from app.Routes import routes_pelicula, routes_categoria

    app.register_blueprint(routes_pelicula.bp)
    app.register_blueprint(routes_categoria.bp)


    return app