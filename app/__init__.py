import os
from flask import Flask
from app.config import Config
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_user import UserManager
from flask_session import Session

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
mail = Mail()
session = Session()


def create_app(config_class=Config):
    app = Flask(__name__)
    config_name = os.environ.get("FLASK_CONFIG", "Dev")
    app.config.from_object(getattr(config, config_name.title() + "Config"))
    app.app_context().push()

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    mail.init_app(app)

    from app.models import User
    user_manager = UserManager(app, db, User)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.online_check import bp as online_check_bp
    app.register_blueprint(online_check_bp)

    return app


from app import models
