from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    CORS(app)
    db.init_app(app)

    from .routes.webhooks import webhook_bp
    from .routes.admin_api import admin_bp
        from .routes.unsubscribe import unsub_bp
    from .routes.auth import auth_bp
    from .routes.app_proxy import app_proxy_bp
    from .tasks.scheduler import tasks_bp

    app.register_blueprint(webhook_bp)
            app.register_blueprint(admin_bp)
        app.register_blueprint(unsub_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(app_proxy_bp)
    app.register_blueprint(tasks_bp)

    with app.app_context():
        from . import models  # ensure models are imported
        db.create_all()

    return app