from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    medicine1 = Medicine.query.all()

    if request.method == 'POST':
        name = request.form.get('name')
        medicine = Medicine.query.filter_by(mName=name).first()
        if medicine:
            flash('Medicine already exists.', category='error')
        else:
            new_medicine = Medicine(mName=name)
            db.session.add(new_medicine)
            db.session.commit()
            flash('Account created!', category='success')

            return redirect(url_for('auth.sign_up'))

    return render_template("sign_up.html", medicine=medicine1 )

