from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager

from .models import UserModel

from .config import Config
from .auth import auth


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Que te loguies papi'
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    bootstrap = Bootstrap5(app)
    login_manager.init_app(app)
    
    app.register_blueprint(auth)

    return app
