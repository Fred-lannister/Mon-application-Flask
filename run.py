# run.py

import os
from app import create_app
from models import db
from models import User, Transaction, Objectif

from dotenv import load_dotenv
load_dotenv()

# Créez l'instance de l'application
app = create_app()

# Si vous voulez lancer l'application directement avec `python run.py`
if __name__ == '__main__':
    app.run(debug=True)

# Contexte pour le shell, utile pour les commandes flask db
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Transaction': Transaction, 'Objectif': Objectif}



