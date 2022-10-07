"""
Initialization file for the irawo_meals package
"""

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Allow permanent sessions
app.config["SESSION_PERMANENT"] = True

# Set up user sessions from flask_session
Session(app)

# Set secret key for session cookies
app.config["SECRET_KEY"] = '1221bce241e2cc3edee7d2d3d93568a8'


# Import app routes AFTER initial setup to prevent import issues
from irawo_meals import routes