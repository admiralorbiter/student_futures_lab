"""Application configuration."""

import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(DATA_DIR, 'student_responses.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Path to YAML mapping files
    MAPPINGS_DIR = os.path.join(DATA_DIR, "mappings")

    # Cookie settings for optional student code
    STUDENT_CODE_COOKIE = "student_code"
    STUDENT_CODE_MAX_AGE = 60 * 60 * 24 * 30  # 30 days
