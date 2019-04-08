from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField, TextAreaField

class CreateRequestForm(FlaskForm):
    firstname = StringField('Vorname')
    lastname = StringField('Nachname')
    email = StringField('E-Mail Adresse')
    tel = StringField('Telefon-Nr.')

    model = StringField('Gerätebezeichnung')
    manufakturer = StringField('Hersteller')
    category = SelectField('Kategorie', choices=[])

    error_description = TextAreaField('Fehlerbeschreibung')

    submit = SubmitField(u'Speichern')

    def set_categories(self, categories):
        self.category.choices = [(c.name, c.name + ' ' + c.samples) for c in categories]
