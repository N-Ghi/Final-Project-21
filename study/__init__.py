from flask import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import os

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
s = URLSafeTimedSerializer('your_secret_key')

def create_app():
    app = Flask(__name__)
    app.config.from_object('study.config.Config')


    db_path = 'study.db'
    if os.path.exists(db_path):
        os.remove(db_path)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    from study.db_models import User
    from .routes import register_routes

    @login_manager.user_loader
    def load_user(username):
        return User.query.get(username)

    with app.app_context():
        db.create_all()

    register_routes(app)
    
    return app

def generate_confirmation_token(email):
    return s.dumps(email, salt='email-confirmation-salt')

def confirm_token(token, expiration=3600):
    try:
        email = s.loads(token, salt='email-confirmation-salt', max_age=expiration)
    except:
        return False
    return email

def send_confirmation_email(user_email):
    token = generate_confirmation_token(user_email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('email/activate.html', confirm_url=confirm_url)
    msg = Message('Please confirm your email', recipients=[user_email])
    msg.html = html
    mail.send(msg)