# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators

class PetForm(FlaskForm):
    submit = SubmitField('Checkout')


class CardForm(FlaskForm):
    card_number = StringField('Card Number', [validators.DataRequired(), validators.Length(min=16, max=16)])
    expiration_date = StringField('Expiration Date (MM/YY)', [validators.DataRequired(), validators.Length(min=5, max=5)])
    cvv = StringField('CVV', [validators.DataRequired(), validators.Length(min=3, max=3)])
    submit = SubmitField('Complete Checkout')
