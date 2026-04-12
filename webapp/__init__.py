import sys
from pathlib import Path

from flask import Flask

from .routes import bp
from .services.job_manager import JobManager


def _resolve_webapp_dir():
    module_dir = Path(__file__).resolve().parent
    candidates = [module_dir]

    meipass_dir = getattr(sys, "_MEIPASS", None)
    if meipass_dir:
        candidates.append(Path(meipass_dir) / "webapp")

    candidates.append(Path(sys.executable).resolve().parent / "webapp")

    for candidate in candidates:
        if (candidate / "templates" / "index.html").exists() and (candidate / "static").exists():
            print(f"[webapp] template root selected: {candidate}")
            return candidate

    print(f"[webapp] template root fallback: {module_dir}")
    return module_dir


def create_app():
    webapp_dir = _resolve_webapp_dir()
    app = Flask(
        __name__,
        template_folder=str(webapp_dir / "templates"),
        static_folder=str(webapp_dir / "static"),
    )
    print(
        "[webapp] Flask paths:",
        f"root={app.root_path}",
        f"templates={app.template_folder}",
        f"static={app.static_folder}",
    )
    app.config["SECRET_KEY"] = "tcdd-web-app-dev"
    app.job_manager = JobManager()
    app.register_blueprint(bp)
    return app
