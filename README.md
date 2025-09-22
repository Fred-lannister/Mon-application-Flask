# Mon Assistant Financier IA 🧠
Mon Assistant Financier IA est une application web de gestion financière personnelle conçue pour vous aider à suivre vos finances, à atteindre vos objectifs d'épargne et à obtenir des conseils personnalisés grâce à l'intelligence artificielle générative.

L'objectif principal est de fournir une solution intuitive qui simplifie la gestion de votre budget quotidien et vous offre des insights financiers intelligents.

## Fonctionnalités principales
**Tableau de bord :** Visualisez votre solde, vos revenus et vos dépenses mensuelles à l'aide de graphiques interactifs (solde, dépenses par catégorie, et dépenses mensuelles).

**Transactions :** Enregistrez et suivez facilement toutes vos transactions (dépenses et revenus).

**Assistant IA conversationnel :** Posez des questions à votre assistant IA alimenté par l'API Gemini et recevez des réponses et des conseils financiers en temps réel.

**Objectifs financiers :** Créez et suivez la progression de vos objectifs d'épargne (par exemple, "Voyage", "Voiture").

**Gestion de profil :** Personnalisez votre profil en téléchargeant une photo de profil.

## Technologies
*Backend : Python, Flask*

**Base de données :** SQLite avec SQLAlchemy

**Frontend :** HTML, CSS (Bootstrap), JavaScript (Chart.js)

**IA : Google Gemini API**

**Autres : Flask-Login, Flask-Migrate**

## Installation
Clonez le dépôt :
git clone https://github.com/Fred-lannister/Mon-application-Flask.git

Installez les dépendances :
pip install -r requirements.txt

Configurez vos variables d'environnement (.env) pour la clé secrète de Flask et la clé API de Gemini.

Lancez les migrations de la base de données :

flask db migrate -m "Initialisation de la base de données"

flask db upgrade

Démarrez l'application :
flask run

**Contact :** njomanifred@gmail.com/fred.njomani@ensea.edu.ci 
