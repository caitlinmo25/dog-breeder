# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField
from forms import PetForm, CardForm
import os
import requests
app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Oranges25!@127.0.0.1:5432/postgres' #PSQL passwo
db = SQLAlchemy(app)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    price = db.Column(db.Float)

class PetForm(FlaskForm):
    submit = SubmitField('Checkout')

@app.route('/')
def index():
    pets = Pet.query.all()
    return render_template('index.html', pets=pets)

@app.route('/pet/<int:pet_id>', methods=['GET'])
def pet(pet_id):
    pet = Pet.query.get(pet_id)
    form = PetForm()
    access_key ='338489e055100d46da834038f2a679a6' #We need to put the API key here
    response = requests.get(f"http://api.exchangerate.host/convert?from=USD&to=EUR&amount={pet.price}&access_key={access_key}")
    data = response.json()
    pet.price = data['result']
    return render_template('pet.html', pet=pet, form=form)

@app.route('/checkout/<int:pet_id>', methods=['GET', 'POST'])
def checkout(pet_id):
    pet = Pet.query.get(pet_id)
    form = CardForm()
    if request.method == 'POST' and form.validate_on_submit():
        db.session.delete(pet)
        db.session.commit()
        flash('Pet has been checked out!', 'success')
        return redirect(url_for('index'))
    return render_template('checkout.html', pet=pet, form=form)

if __name__ == '__main__':
    app.run()

