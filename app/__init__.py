from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager

from .views.main import main
from .views.auth import auth
# from .models.storage_manager import storage_manager
from .models.db_manager import db_manager
from .models.user import User

def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config['RATELIMIT_HEADERS_ENABLED'] = True
    # app.config['RATELIMIT_STORAGE_URI'] = 'memcached://localhost:11211'
    app.config['RATELIMIT_STORAGE_URI'] = 'memory://'
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # storage_manager.init_storage()
    
    limiter = Limiter(app, key_func=get_remote_address, default_limits=["1000/day;500/hour;100/minute;10/second"])

    app.register_blueprint(main)
    app.register_blueprint(auth)

    db_manager.init_db(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
