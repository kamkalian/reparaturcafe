from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, BooleanField

class NewOnlineCheckForm(FlaskForm):
    customer_name = StringField('Name')
    customer_email = StringField('E-Mail Adresse')
    customer_tel = StringField('Telefonnummer')
    device_name = StringField('Gerätename/Modell/Hersteller')
    device_issue = TextAreaField('Fehlerbeschreibung')
    device_opened = BooleanField('Wurde das Gerät schon einmal aufgeschraubt?')
    device_manual = BooleanField('Ist eine Bedienungsanleitung vorhanden?')
    submit = SubmitField('Abschicken')
