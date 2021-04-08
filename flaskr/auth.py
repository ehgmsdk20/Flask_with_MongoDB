import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flask_mongoengine.wtf import model_form

from flask_login import login_user, login_required, logout_user

from .models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

UserForm = model_form(User, field_args={'password': {'password': True}})
@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = UserForm(request.form)
    if request.method == 'POST':
        existing_user = User.objects(username=form.username.data).first()
        if existing_user is None:
            hashpass = generate_password_hash(form.password.data)
            User(username=form.username.data,password=hashpass).save()
            return redirect(url_for('auth.login'))
        else:
            flash('Already registered username')

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = UserForm(request.form)
    if request.method == 'POST':
        user = User.objects(username=form.username.data).first()
        if user:
                if check_password_hash(user['password'], form.password.data):
                    login_user(user)
                    flash('Logged in successfully.')
                    return redirect(url_for('index'))
        flash('Invalid username or password')

    return render_template('auth/login.html')

@bp.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
