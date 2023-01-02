from flask_sqlalchemy import SQLAlchemy

class DBManager():
    def __init__(self):
        self.__db = SQLAlchemy()

    def init_db(self, app):
        self.__db.init_app(app)

    def create_db(self):
        self.__db.create_all()

    def get_db_model(self):
        return self.__db.Model

    def get_user_columns(self):
        return \
            self.__db.Column(self.__db.Integer, primary_key=True), \
            self.__db.Column(self.__db.String(128), unique=True), \
            self.__db.Column(self.__db.String(128)), \
            self.__db.Column(self.__db.String(256)), \
            self.__db.Column(self.__db.Integer)

    def add_user(self, user):
        is_success = False
        try:
            self.__db.session.add(user)
            self.__db.session.commit()
            is_success = True
        except:
            self.__db.session.rollback()
            is_success = False
        return is_success

db_manager = DBManager()
