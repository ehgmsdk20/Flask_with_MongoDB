import functools

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flask_mongoengine.wtf import model_form

from flask_login import login_user, login_required, logout_user, current_user

from .models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

UserForm = model_form(User, field_args={'password': {'password': True}})
@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = UserForm(request.form)
    if request.method == 'POST':
        existing_user = User.objects(user_id=form.user_id.data).first()
        if existing_user is None:
            hashpass = generate_password_hash(form.password.data)
            User(user_id=form.user_id.data,password=hashpass).save()
            return redirect(url_for('auth.login'))
        else:
            flash('Already registered ID')

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = UserForm(request.form)
    if request.method == 'POST':
        user = User.objects(user_id=form.user_id.data).first()
        if user:
                if check_password_hash(user['password'], form.password.data):
                    login_user(user)
                    return redirect(url_for('index'))
        flash('Invalid ID or password')

    return render_template('auth/login.html')

@bp.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/unregister', methods = ['GET'])
@login_required
def unregister():
    User.objects(user_id = current_user.user_id).first().delete()
    return redirect(url_for('blog.index'))