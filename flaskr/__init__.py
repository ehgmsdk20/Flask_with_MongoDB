import os

from flask import Flask

from flask_login import LoginManager

from .models import db, User

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        #SECRET_KEY = os.urandom(24),
    )
    app.config['MONGODB_SETTINGS'] = {
        "db": "Dummy_Project",
    }
    db.init_app(app)
    login_manager = LoginManager(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(pk=user_id).first()

    from . import auth
    app.register_blueprint(auth.bp)
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from flask import render_template
    @app.route('/')
    def index():
        return render_template('base.html')


    return app