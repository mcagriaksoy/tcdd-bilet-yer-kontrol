from flask import Flask

from .routes import bp
from .services.job_manager import JobManager


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "tcdd-web-app-dev"
    app.job_manager = JobManager()
    app.register_blueprint(bp)
    return app
