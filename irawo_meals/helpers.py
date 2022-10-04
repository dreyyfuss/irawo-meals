"""
Assisting functions
"""

import sqlite3

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


def is_admin():
    """
    Returns true if the logged in user is an admin
    """
    # Connect to lessons database
    con = sqlite3.connect("app.db")

    with con:

        # Set to read database rows as dictionaries
        con.row_factory = sqlite3.Row
        db = con.cursor()

        # Get admin status of current user from database
        db.execute("SELECT admin_status FROM users WHERE id = ?", (session["user_id"]))
        admin = db.fetchone()["admin_status"]

    if admin == "t":
        return True
    else:
        return False