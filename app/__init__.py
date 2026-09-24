import os
from pathlib import Path

import click
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS

from .extensions import db


def create_app(test_config=None):
    root = Path(__file__).resolve().parent.parent
    load_dotenv(root / ".env")

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY", "development-only-change-me"),
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "DATABASE_URL",
            "mysql+pymysql://pezeshkafzar:replace-password@127.0.0.1:3306/pezeshkafzar_journal?charset=utf8mb4",
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ENGINE_OPTIONS={"pool_pre_ping": True, "pool_recycle": 280},
        TOKEN_MAX_AGE=int(os.getenv("TOKEN_MAX_AGE", "43200")),
        UPLOAD_FOLDER=str(root / "uploads"),
        MAX_CONTENT_LENGTH=int(os.getenv("MAX_UPLOAD_MB", "8")) * 1024 * 1024,
        AUTO_CREATE_SCHEMA=os.getenv("AUTO_CREATE_SCHEMA", "true").lower() == "true",
    )
    if test_config:
        app.config.update(test_config)
        if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
            app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {}

    db.init_app(app)
    origins = [item.strip() for item in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",") if item.strip()]
    CORS(app, resources={r"/api/*": {"origins": origins}})

    from .auth import bp as auth_bp
    from .articles import bp as articles_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(articles_bp)

    register_commands(app)

    @app.get("/api/health")
    def health():
        return jsonify(status="ok")

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify(message="مسیر یا مقاله پیدا نشد."), 404

    @app.errorhandler(413)
    def too_large(_error):
        return jsonify(message="حجم تصویر بیشتر از حد مجاز است."), 413

    if app.config["AUTO_CREATE_SCHEMA"]:
        with app.app_context():
            db.create_all()
            from .models import ArticleCategory
            ArticleCategory.ensure_defaults()

    return app


def register_commands(app):
    from .models import AdminUser, Article
    from .seed import ARTICLES

    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        from .models import ArticleCategory
        ArticleCategory.ensure_defaults()
        click.echo("Database tables are ready.")

    @app.cli.command("create-admin")
    @click.option("--username", prompt=True)
    @click.password_option(confirmation_prompt=True)
    def create_admin(username, password):
        username = username.strip()
        user = AdminUser.query.filter_by(username=username).first() or AdminUser(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f"Admin '{username}' is ready.")

    @app.cli.command("seed-articles")
    def seed_articles():
        for payload in ARTICLES:
            item = Article.query.filter_by(slug=payload["slug"]).first() or Article()
            item.apply(payload)
            db.session.add(item)
        db.session.commit()
        click.echo(f"Seeded {len(ARTICLES)} journal articles.")
