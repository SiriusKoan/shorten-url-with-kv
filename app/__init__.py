from flask_login import LoginManager
from flask import Flask
from .config import configs

login_manager = LoginManager()


def create_app(env):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(configs[env])

    login_manager.init(app)

    from .main import main_bp

    app.register_blueprint(main_bp)

    from .admin import admin_bp

    app.register_blueprint(admin_bp)

    from .user import user_bp

    app.register_blueprint(user_bp)
