from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main = Blueprint('main', __name__, url_prefix='/')

@main.route('/', methods=["GET"])
@login_required
def index():
    return render_template('index.html', name=current_user.name)
