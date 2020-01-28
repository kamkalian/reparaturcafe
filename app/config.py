import os
import warnings
from dotenv import load_dotenv
from pathlib import Path


# basedir = os.path.abspath(os.path.dirname(__file__))

app_basedir = Path(__file__).parents[1]
env_file = Path(app_basedir, ".env")

if env_file.exists():
    load_dotenv(env_file)
else:
    warnings.warn("No .env file found.")


def get_env_var(var_name, default=None, rv_type_class=None, *, raise_no_default=True):
    """Func for importing environment variables"""
    var = os.environ.get(var_name, default)

    msg_no_default = f"Environment variable '{var_name}' not set or empty and no default value given."

    if var == "" or var is None:
        if default is not None:
            return default
        elif raise_no_default:
            raise KeyError(msg_no_default) from None
        else:
            warnings.warn(msg_no_default)
            return None

    if rv_type_class is None:
        return var
    elif rv_type_class is bool:
        return var.lower() in {"1", "t", "true"}
        ''' hier gibt es noch einen Fehler,
        wenn z.B. bei bool die var Variable mit False gefüllt ist '''
    return rv_type_class(var)


class Config(object):
    DEBUG = False
    TESTING = False
    APP_NAME = 'reparaturcafe'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guesskjkjkjkjkghgjgfsdfdsfdsfdsf'
    SESSION_TYPE = "filesystem"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMINS = ['oskar@reparaturcafe.kurm.de']

    # Flask-Mail SMTP server settings
    MAIL_SERVER = get_env_var('MAIL_SERVER')
    MAIL_PORT = get_env_var('MAIL_PORT', 587, int)
    MAIL_USE_TLS = get_env_var('MAIL_USE_TLS', False, bool)
    MAIL_USERNAME = get_env_var('MAIL_USERNAME')
    MAIL_PASSWORD = get_env_var('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'oskar@reparaturcafe.kurm.de'
    # print(MAIL_USERNAME, MAIL_PASSWORD, MAIL_PORT, MAIL_SERVER, MAIL_USE_TLS)

#: Flask-User settings
    USER_APP_NAME = 'Reparaturcafe'
    USER_EMAIL_SENDER_NAME = get_env_var('USER_EMAIL_SENDER_NAME', USER_APP_NAME)
    USER_EMAIL_SENDER_EMAIL = get_env_var('USER_EMAIL_SENDER_EMAIL', MAIL_DEFAULT_SENDER)
    USER_AUTO_LOGIN_AFTER_REGISTER = False
    USER_AUTO_LOGIN_AFTER_RESET_PASSWORD = False
    USER_RESET_PASSWORD_EXPIRATION = 10 * 60
    #: Disable unwanted urls
    USER_ENABLE_CHANGE_PASSWORD = False
    USER_ENABLE_CHANGE_USERNAME = False
    USER_ENABLE_MULTIPLE_EMAILS = False
    USER_ENABLE_INVITE_USER = False

    # USER_CONFIRM_EMAIL_TEMPLATE = 'emails/confirm_email'
    # USER_PASSWORD_CHANGED_EMAIL_TEMPLATE = 'emails/password_changed'
    # USER_REGISTERED_EMAIL_TEMPLATE = 'emails/registered'
    # USER_RESET_PASSWORD_EMAIL_TEMPLATE = 'emails/reset_password'
    # USER_USERNAME_CHANGED_EMAIL_TEMPLATE = 'emails/username_changed'

    USER_CONFIRM_EMAIL_URL = '/auth/confirm-email/<token>'
    USER_AFTER_CONFIRM_ENDPOINT = 'main.index'

    USER_FORGOT_PASSWORD_URL = '/auth/reset-password'
    # USER_FORGOT_PASSWORD_TEMPLATE = 'reset_password.html'
    USER_AFTER_FORGOT_PASSWORD_ENDPOINT = 'user.login'

    USER_LOGIN_URL = '/auth/login'
    # USER_LOGIN_TEMPLATE = 'login.html'
    USER_AFTER_LOGIN_ENDPOINT = 'main.index'

    USER_LOGOUT_URL = '/auth/logout'
    USER_AFTER_LOGOUT_ENDPOINT = 'main.index'

    USER_REGISTER_URL = '/auth/register'
    # USER_REGISTER_TEMPLATE = 'register.html'
    USER_AFTER_REGISTER_ENDPOINT = 'main.index'

    USER_RESEND_EMAIL_CONFIRMATION_URL = '/auth/resend-email-confirmation'
    # USER_RESEND_CONFIRM_EMAIL_TEMPLATE = 'resend_confirm_email.html'
    USER_AFTER_RESEND_EMAIL_CONFIRMATION_ENDPOINT = 'main.index'

    USER_RESET_PASSWORD_URL = '/auth/reset-password/<token>'
    # USER_RESET_PASSWORD_TEMPLATE = 'reset_password.html'
    USER_AFTER_RESET_PASSWORD_ENDPOINT = 'user.login'

    USER_UNAUTHENTICATED_ENDPOINT = 'user.login'

    USER_UNAUTHORIZED_ENDPOINT = ''

    TELEGRAM_BOT_TOKEN = get_env_var('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = get_env_var('TELEGRAM_CHAT_ID')

class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = get_env_var("SECRET_KEY", "not-sufficient-for-production")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(app_basedir, 'reparaturcafe.db')
    print(SQLALCHEMY_DATABASE_URI)


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = get_env_var("SECRET_KEY", "sufficient-for-testsdsfdfgffdgfdgfdgfdgfdgfdg")

    SQLALCHEMY_DATABASE_URI = "sqlite://"


class ProdConfig(Config):
    password = get_env_var("MYSQL_PASSWORD")
    username = get_env_var("MYSQL_USER")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'mysql+pymysql://' + username + ':' + password + '@localhost/reparaturcafe'
    pass
