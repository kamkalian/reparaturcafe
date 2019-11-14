import os
from flask import Flask
from app.config import Config
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_user import UserManager
from flask_session import Session
from telegram.ext import Updater, CommandHandler

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

    updater = Updater(token='1025332314:AAHeb5_PDYFOnPVgyqwiqJXUAQ9B7pz8lJI', use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    list_handler = CommandHandler('list', list)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(list_handler)
    updater.start_polling()

    return app

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hallo Welt')
    print('Hallo Welt')

def list(update, context):
    try:
        oc_list = Onlinecheck.query.filter(
            ~Onlinecheck.logs.any(Log.state=='closed')
        ).all() 
        context.bot.send_message(chat_id=update.effective_chat.id, text=oc_list)
        print(oc_list)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Datenbank nicht erreichbar.')
        print('Error')
    



from app import models
