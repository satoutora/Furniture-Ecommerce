from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        #init_admin(app)
        print('Created database')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Vjp pro'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.app_context().push()
    db.init_app(app)
    app.config["IMAGE_UPLOADS"] = "website/static/uploads/"
    app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
    app.config['WHOOSH_BASE'] = 'whoosh'

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app


def init_admin(app):
    from .models import User
    with app.app_context():
        user = User(user_name = "admin",
                    password = generate_password_hash("admin", method='sha256'),
                    full_name = "Toi La Admin",
                    type_user = 0)
        db.session.add(user)
        print("created admin")
        db.session.commit()