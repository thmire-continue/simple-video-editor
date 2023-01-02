from flask_login import UserMixin
from .db_manager import db_manager

class User(UserMixin, db_manager.get_db_model()):
    id, email, password, name, permission = db_manager.get_user_columns()
