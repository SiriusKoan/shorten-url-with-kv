from flask import Flask
from .config import configs
from .db import db
from .user_helper import login_manager


def create_app(env):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(configs[env])

    login_manager.init_app(app)
    db.init_app(app)

    from .main import main_bp

    app.register_blueprint(main_bp)

    from .admin import admin_bp

    app.register_blueprint(admin_bp)

    from .user import user_bp

    app.register_blueprint(user_bp)

    return app
