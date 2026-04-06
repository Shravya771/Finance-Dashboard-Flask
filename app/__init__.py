import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv
from config import Config

load_dotenv()

# ===============================
# GLOBAL EXTENSIONS (VERY IMPORTANT)
# ===============================
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "templates"
        )
    )

    app.config.from_object(Config)

    # ===============================
    # INIT EXTENSIONS
    # ===============================
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    # ===============================
    # BASIC ROUTES (HTML PAGES)
    # ===============================
    @app.route("/")
    def login_page():
        return render_template("login.html")

    @app.route("/dashboard")
    def dashboard_page():
        return render_template("dashboard.html")

    @app.route("/check")
    def check():
        return {"msg": "server working"}

    # ===============================
    # BLUEPRINTS (IMPORTANT)
    # ===============================
    from app.routes.auth_routes import auth_bp
    from app.routes.finance_routes import finance_bp
    from app.routes.user_routes import user_bp   # ✅ ADDED

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(finance_bp, url_prefix="/finance")
    app.register_blueprint(user_bp, url_prefix="/users")   # ✅ ADDED

    return app