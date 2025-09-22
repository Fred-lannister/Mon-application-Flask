# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, DateField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    password_confirm = PasswordField(
        'Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('S\'inscrire')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Ce nom d\'utilisateur est déjà pris. Veuillez en choisir un autre.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Cet email est déjà utilisé. Veuillez en choisir un autre.')
        
class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class TransactionForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    amount = FloatField('Montant (FCFA)', validators=[DataRequired()])
    category = SelectField('Catégorie', choices=[
        ('Alimentation', 'Alimentation'),
        ('Transport', 'Transport'),
        ('Loisirs', 'Loisirs'),
        ('Factures', 'Factures'),
        ('Santé', 'Santé'),
        ('Shopping', 'Shopping'),
        ('Logement', 'Logement'),
        ('Salaire', 'Salaire'),
        ('Autre', 'Autre')
    ], validators=[DataRequired()])
    date = DateField('Date (YYYY-MM-DD)', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Ajouter')

class ObjectifForm(FlaskForm):
    name = StringField('Nom de l\'objectif', validators=[DataRequired()])
    target_amount = FloatField('Montant cible (FCFA)', validators=[DataRequired()])
    current_amount = FloatField('Montant actuel (FCFA)', default=0.0)
    submit = SubmitField('Ajouter l\'objectif')









