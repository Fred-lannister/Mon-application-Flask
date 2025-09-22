# config.py


import os
from dotenv import load_dotenv

# Charger automatiquement le fichier .env
load_dotenv()

class Config:
    # Clé secrète pour les sessions et les protections CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Configuration de la base de données (cohérence avec .env)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance/finance.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuration de l'API Gemini
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') 

