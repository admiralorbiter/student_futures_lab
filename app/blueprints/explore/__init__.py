"""Explore blueprint — data explorer with charts and drill-down views."""

from flask import Blueprint

bp = Blueprint("explore", __name__, url_prefix="/explore")

from . import routes  # noqa: E402, F401
