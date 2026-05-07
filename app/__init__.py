from flask import Flask
from dotenv import load_dotenv

from .config import Config
from .extensions import db, login_manager, csrf, migrate


def create_app(config_class: type = Config) -> Flask:
    load_dotenv()

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    from .models import User

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(User, int(user_id))

    from .routes.main import main_bp
    from .routes.auth import auth_bp
    from .routes.shop import shop_bp
    from .routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(shop_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.context_processor
    def inject_cart_count():
        from flask import session
        cart = session.get("cart", {})
        return {"cart_count": sum(cart.values()) if cart else 0}

    with app.app_context():
        db.create_all()
        _seed_admin(app)

    return app


def _seed_admin(app: Flask) -> None:
    from .models import User
    from werkzeug.security import generate_password_hash

    email = app.config["ADMIN_EMAIL"]
    if not User.query.filter_by(email=email).first():
        admin = User(
            email=email,
            full_name="Administrator",
            password_hash=generate_password_hash(app.config["ADMIN_PASSWORD"]),
            is_admin=True,
        )
        db.session.add(admin)
        db.session.commit()
        app.logger.info("Seeded default admin: %s", email)
