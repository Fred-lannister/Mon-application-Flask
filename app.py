# app.py

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialisation des extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Importations des modèles et des routes APRES l'initialisation de db
    from models import User, Transaction, Objectif
    from routes import main
    
    # Enregistrement des Blueprints
    app.register_blueprint(main)

    return app

# Charger id de l'utilisateur
@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))


