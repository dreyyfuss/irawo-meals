"""
Initialization file for the irawo_meals package
"""

from flask import Flask
from flask_session import Session
from werkzeug.middleware.proxy_fix import ProxyFix

from irawo_meals.helpers import format_weekday


# Configure application
app = Flask(__name__)

# Tell flask it is behind a proxy
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

# Custom filter
app.jinja_env.filters["weekday"] = format_weekday

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Allow permanent sessions
app.config["SESSION_PERMANENT"] = True

# Set session backend type
app.config["SESSION_TYPE"] = "filesystem"

# Set up user sessions from flask_session
Session(app)

# Set secret key for session cookies
app.config["SECRET_KEY"] = '1221bce241e2cc3edee7d2d3d93568a8'


# Import app routes AFTER initial setup to prevent import issues
from irawo_meals import routes