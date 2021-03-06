from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class UserEditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    lastname = StringField('Nachname')
    firstname = StringField('Vorname')
    email = StringField('E-Mail Adresse', validators=[DataRequired(), Email()])
    submit = SubmitField('Speichern')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different username.')
    #
    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is not None:
    #         raise ValidationError('Please use a different email address.')
