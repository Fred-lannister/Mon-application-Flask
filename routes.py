from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from forms import RegistrationForm, LoginForm, TransactionForm, ObjectifForm
from models import User, Transaction, Objectif
from app import db
from utils import generate_financial_data
from sqlalchemy import func, case
from datetime import date, timedelta
import json
from ai_service import get_ai_response

main = Blueprint('main', __name__)

# Fonction utilitaire pour collecter toutes les données du tableau de bord
def get_dashboard_data(user_id):
    """Collecte toutes les données nécessaires pour le tableau de bord, en limitant les transactions à 10."""
    user_transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date.desc()).limit(10).all()
    
    # Calcul des KPI
    total_balance = db.session.query(func.sum(Transaction.amount)).filter_by(user_id=user_id).scalar() or 0
    start_of_month = date.today().replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    monthly_income = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.amount > 0,
        Transaction.date >= start_of_month,
        Transaction.date <= end_of_month
    ).scalar() or 0
    
    monthly_expenses = db.session.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.amount < 0,
        Transaction.date >= start_of_month,
        Transaction.date <= end_of_month
    ).scalar() or 0
    
    recent_transaction = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date.desc()).first()

    # Données pour le graphique de dépenses par catégorie
    expenses_data = db.session.query(
        Transaction.category,
        func.sum(case((Transaction.amount < 0, Transaction.amount), else_=0))
    ).filter(
        Transaction.user_id == user_id,
        Transaction.amount < 0
    ).group_by(Transaction.category).all()
    
    expenses_labels = json.dumps([data[0] for data in expenses_data])
    expenses_values = json.dumps([abs(data[1]) for data in expenses_data])

    # Données pour l'évolution du solde
    balance_data = db.session.query(
        func.date(Transaction.date),
        func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == user_id
    ).group_by(func.date(Transaction.date)).order_by(func.date(Transaction.date)).all()
    
    balance_labels = json.dumps([row[0] for row in balance_data])
    balance_values = json.dumps([row[1] for row in balance_data])

    # Données pour le graphique des dépenses mensuelles
    monthly_expenses_data = db.session.query(
        func.strftime('%Y-%m', Transaction.date),
        func.sum(case((Transaction.amount < 0, Transaction.amount), else_=0))
    ).filter(
        Transaction.user_id == user_id
    ).group_by(func.strftime('%Y-%m', Transaction.date)).order_by(func.strftime('%Y-%m', Transaction.date)).all()

    monthly_expenses_labels = json.dumps([row[0] for row in monthly_expenses_data])
    monthly_expenses_values = json.dumps([abs(row[1]) for row in monthly_expenses_data])

    return {
        'total_balance': total_balance,
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'recent_transaction': recent_transaction,
        'user_transactions': user_transactions,
        'expenses_labels': expenses_labels,
        'expenses_values': expenses_values,
        'balance_labels': balance_labels,
        'balance_values': balance_values,
        'monthly_expenses_labels': monthly_expenses_labels,
        'monthly_expenses_values': monthly_expenses_values
    }

@main.route('/')
def homepage():
    return render_template('pages/homepage.html')

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = Transaction(
            description=form.description.data,
            amount=form.amount.data,
            category=form.category.data,
            date=form.date.data,
            owner=current_user
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction ajoutée avec succès !', 'success')
        return redirect(url_for('main.dashboard'))
    
    data = get_dashboard_data(current_user.id)
    return render_template('pages/dashboard.html', form=form, **data)

@main.route('/generate-data', methods=['POST'])
@login_required
def generate_data():
    try:
        generate_financial_data(current_user.id)
        return jsonify({'message': 'Données générées avec succès !'}), 200
    except Exception as e:
        return jsonify({'message': f'Une erreur est survenue : {e}'}), 500

@main.route('/clear-data', methods=['POST'])
@login_required
def clear_data():
    try:
        Transaction.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        return jsonify({'message': 'Toutes les données de transaction ont été effacées.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Une erreur est survenue lors de l\'effacement des données : {e}'}), 500

# Routes d'authentification
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Nom d\'utilisateur ou mot de passe invalide', 'danger')
            return redirect(url_for('main.login'))
        login_user(user)
        flash('Connexion réussie!', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('auth/login.html', form=form)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Félicitations, vous êtes maintenant un utilisateur enregistré !', 'success')
        return redirect(url_for('main.login'))
    return render_template('auth/register.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('main.homepage'))

# Route du chat
@main.route('/chat')
@login_required
def chat():
    return render_template('chat/chat.html')

@main.route('/chat_api', methods=['POST'])
@login_required
def chat_api():
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'response': 'Veuillez poser une question.'}), 400
    ai_response = get_ai_response(user_message)
    return jsonify({'response': ai_response})

@main.route('/recommandations')
@login_required
def recommandations():
    return render_template('pages/recommandations.html')

@main.route('/objectifs', methods=['GET', 'POST'])
@login_required
def objectifs():
    form = ObjectifForm()
    if form.validate_on_submit():
        objectif = Objectif(
            name=form.name.data,
            target_amount=form.target_amount.data,
            current_amount=form.current_amount.data,
            user_id=current_user.id
        )
        db.session.add(objectif)
        db.session.commit()
        flash('Objectif ajouté avec succès !', 'success')
        return redirect(url_for('main.objectifs'))
    user_objectifs = Objectif.query.filter_by(user_id=current_user.id).all()
    return render_template('pages/objectifs.html', objectifs=user_objectifs, form=form)

@main.route('/profil')
@login_required
def profil():
    return render_template('pages/profil.html')


