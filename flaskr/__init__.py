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

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')


    return app