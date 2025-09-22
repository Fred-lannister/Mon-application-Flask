# utils.py

from faker import Faker
import random
from datetime import datetime, timedelta
from app import db
from models import Transaction

def generate_financial_data(user_id, count=20):
    """
    Génère un jeu de données synthétiques de transactions et les ajoute à la base de données.
    """
    fake = Faker('fr_FR')
    
    categories_depenses = [
        'Alimentation', 'Transport', 'Loisirs', 'Factures', 'Santé', 
        'Shopping', 'Logement', 'Voyages'
    ]
    categories_revenus = ['Salaire', 'Bonus', 'Freelance', 'Cadeau']
    
    start_date = datetime.utcnow() - timedelta(days=365)
    
    try:
        for _ in range(count):
            is_expense = random.choice([True, False])
            
            if is_expense:
                amount = round(random.uniform(-500.0, -5.0), 2)
                category = random.choice(categories_depenses)
                description = fake.sentence(nb_words=5)
            else:
                amount = round(random.uniform(20.0, 5000.0), 2)
                category = random.choice(categories_revenus)
                description = fake.sentence(nb_words=5)

            # S'assurer que la date est dans le bon format et liée à l'utilisateur
            transaction = Transaction(
                date=fake.date_time_between(start_date=start_date, end_date="now"),
                amount=amount,
                description=description,
                category=category,
                user_id=user_id
            )
            db.session.add(transaction)
            
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Annuler la transaction en cas d'erreur
        raise e  # Relancer l'exception pour la gérer dans la route
    

