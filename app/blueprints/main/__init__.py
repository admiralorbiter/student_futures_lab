"""Main blueprint — landing page and 5 inquiry screens."""

from flask import Blueprint

bp = Blueprint("main", __name__)

from . import routes  # noqa: E402, F401
