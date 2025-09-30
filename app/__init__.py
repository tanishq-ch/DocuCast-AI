# app/__init__.py

import os
from flask import Flask
from config import Config
from app.extensions import db, migrate, bcrypt, login_manager

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints
    from app.auth.routes import auth_bp
    from app.core.routes import core_bp
    from app.main.routes import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(core_bp, url_prefix='/core')

    return app
