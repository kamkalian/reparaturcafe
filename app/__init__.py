import os
from flask import Flask
from app.config import Config, DevConfig
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


def create_app(config_class=None):
    app = Flask(__name__)
    #app.config.from_object(getattr(config, config_name.title() + "Config"))
    if config_class is None:
        config_name = os.environ.get("FLASK_CONFIG")
        if config_name:
            config_class = getattr(config, config_name.title() + "Config")
        else:
            config_class = DevConfig
    app.config.from_object(config_class)
    app.app_context().push()

    print(config_class)

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

    from app.oskar_bot import bp as oskar_bot_bp
    app.register_blueprint(oskar_bot_bp)

    return app


from app import models
