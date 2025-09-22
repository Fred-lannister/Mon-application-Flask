# ai_service.py

import os
import google.generativeai as genai
from config import Config
from flask_login import current_user
from models import Transaction, Objectif
from sqlalchemy import func
import json

def get_ai_response(prompt):
    """
    Appelle le modèle d'IA pour obtenir une réponse à une question donnée.
    """
    genai.configure(api_key=Config.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    try:
        # Récupération des données financières de l'utilisateur
        transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).limit(20).all()
        objectifs = Objectif.query.filter_by(user_id=current_user.id).all()
        
        # Formatage des données pour l'IA
        transactions_data = [{"description": t.description, "montant": t.amount, "categorie": t.category, "date": t.date.strftime('%Y-%m-%d')} for t in transactions]
        objectifs_data = [{"nom": o.name, "cible": o.target_amount, "actuel": o.current_amount} for o in objectifs]

        data_financieres = {
            "transactions_recentes": transactions_data,
            "objectifs_financiers": objectifs_data
        }
        
        # Création d'un prompt complet avec les données et les instructions
        system_instruction = (
            "Tu es un assistant financier IA expert. Ton rôle est de fournir des conseils personnalisés, "
            "de répondre aux questions et d'analyser les données financières fournies par l'utilisateur. "
            "Utilise les données pour donner des conseils précis. Réponds de manière concise et utile. "
            "Si les données ne sont pas pertinentes, fournis un conseil financier général."
            "Pour les conseils il est préférable de les fournir sous forme de liste."
        )

        full_prompt = (
            f"{system_instruction}\n\n"
            f"Voici les données financières de l'utilisateur:\n{json.dumps(data_financieres, indent=2)}\n\n"
            f"Réponds à la question suivante de l'utilisateur: {prompt}"
        )
        
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        print(f"Erreur lors de l'appel à l'API de l'IA: {e}")
        # Message plus explicite pour le débogage
        return "Je suis désolé, je n'ai pas pu générer de réponse pour le moment. L'API est peut-être inaccessible ou votre clé est invalide."
    

    