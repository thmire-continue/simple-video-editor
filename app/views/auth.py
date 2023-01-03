import os
from dotenv import load_dotenv, find_dotenv, set_key

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash, generate_password_hash

from ..models.auth_info import PermissionLevel
from ..models.db_manager import db_manager
from ..models.user import User

auth = Blueprint('auth', __name__, url_prefix='/')

def set_master_administrator(email, password):
    try:
        dotenv_file = find_dotenv()
        load_dotenv(dotenv_file, override=True)
        if (email != os.environ['MASTER_ADMIN_MAIL']) | (password != os.environ['MASTER_ADMIN_PASSWORD']):
            return

        master_administrator = User.query.filter_by(email=email).first()
        if master_administrator:
            return

        name = 'master administrator'
        master_administrator = User(email=email, name=name, password=generate_password_hash(password), permission=PermissionLevel.MASTER_ADMIN)
        is_success = db_manager.add_user(master_administrator)
        if is_success:
            set_key(dotenv_file, 'MASTER_ADMIN_MAIL', '')
            set_key(dotenv_file, 'MASTER_ADMIN_PASSWORD', '')
        else:
            pass # If registing to db was failed, the master administrator info leaves .env file.
    except Exception:
        pass # If occuring unexpected exceptions in this function, do nothing(return None).

    return

@login_required
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.permission != PermissionLevel.MASTER_ADMIN:
        return redirect(url_for('auth.login')), 403

    if request.method == 'POST':
        try:
            email = request.form.get('email')
            name = request.form.get('name')
            password = request.form.get('password')

            user = User.query.filter_by(email=email).first()
            if user:
                return redirect(url_for('auth.register'))

            new_user = User(email=email, name=name, password=generate_password_hash(password), permission=PermissionLevel.USER)
            is_success = db_manager.add_user(new_user)

            if is_success:
                return redirect(url_for('auth.login'))
            else:
                return redirect(url_for('auth.register'))
        except Exception:
            return redirect(url_for('auth.register'))
    else:
        return render_template('registration.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            remember = True if request.form.get('remember') else False

            set_master_administrator(email, password)
            user = User.query.filter_by(email=email).first()
            if not user:
                flash('Please check your login details and try again.')
                return redirect(url_for('auth.login', is_authenticated=False))

            if not check_password_hash(user.password, password):
                flash('Please check your login details and try again.')
                return redirect(url_for('auth.login', is_authenticated=False))

            login_user(user, remember=remember)
            return redirect(url_for('main.index'))
        else:
            if current_user.is_authenticated:
                return redirect(url_for('main.index', is_authenticated=True))
            else:
                return render_template('login.html')
    except Exception:
        return redirect(url_for('auth.login', is_authenticated=False))

@auth.route('/logout')
@login_required
def logout():
    try:
        logout_user()
    except Exception:
        pass
    return redirect(url_for('auth.login'))
