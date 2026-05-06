import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")

    # Use DATABASE_URL if provided (Azure SQL in QA/Prod), else local SQLite.
    DATABASE_URL = os.environ.get("DATABASE_URL") or f"sqlite:///{BASE_DIR / 'app.db'}"
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Seed admin
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@shop.local")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "changeme")
