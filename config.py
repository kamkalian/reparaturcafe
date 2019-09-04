import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    password = os.environ.get("MYSQL_PASSWORD")
    username = os.environ.get("MYSQL_USER")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'mysql+pymysql://' + username + ':' + password + '@localhost/reparaturcafe'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMINS = ['oskar@reparaturcafe.kurm.de']

    # Flask-Mail SMTP server settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'oskar@reparaturcafe.kurm.de'
    print(MAIL_USERNAME, MAIL_PASSWORD, MAIL_PORT, MAIL_SERVER, MAIL_USE_TLS)

#: Flask-User settings
    USER_APP_NAME = 'Reparaturcafe'
    USER_EMAIL_SENDER_NAME = os.environ.get(
        'USER_EMAIL_SENDER_NAME') or USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = os.environ.get(
        'USER_EMAIL_SENDER_EMAIL') or MAIL_DEFAULT_SENDER
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
