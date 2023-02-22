"""
Assisting functions
"""

import calendar
from datetime import datetime, date
from flask import redirect, session
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Decorate routes to require admin login
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect("/logout")
        return f(*args, **kwargs)
    return decorated_function


def management_required(f):
    """
    Decorates routes to require management login
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_management"):
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def format_weekday(date):
    """Format value as USD."""
    day = date.weekday()
    yymmdd = str(date).split("-")
    formatted = f"{calendar.day_name[day][:3]} ({yymmdd[2]}/{yymmdd[1]})"

    return formatted