
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():

    app = Flask("percentpoll")
    
    app.config['SECRET_KEY'] = '\x14\x8b\xe8m\x88(\xc4!\xfe\x05!\xb9'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        with db.session.no_autoflush:
            userId=User.query.get(int(user_id))
        return userId

    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
