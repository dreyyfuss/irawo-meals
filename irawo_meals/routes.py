"""
App routes for the irawo-meals webapp
"""

from flask import flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from irawo_meals import app
from irawo_meals.helpers import admin_required, login_required, management_required


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Log user in
    """
    return render_template()


@app.route("/logout")
def logout():
    """
    Log user out
    """

    # Forget any user_id
    session.clear()

    # Redirect user to login page
    return redirect("/login")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """
    Display form for meal ticking
    """
    return render_template()


@app.route("/personal_history", methods=["GET", "POST"])
@login_required
def personal_history():
    """
    Display meal ticking history for user between selected dates
    """
    return render_template()


@app.route("/account")
@login_required
def account():
    """
    Allows user to manage account (change password)
    """
    return render_template()


@app.route("/meal_count")
@login_required
def meal_count():
    """
    Shows meal count for the day
    """
    return render_template()


@app.route("/general_history", methods=["GET", "POST"])
@login_required
def general_history():
    """
    Display ticking history for all active users between two dates
    """
    return render_template()


@app.route("/manage_users", methods=["GET", "POST"])
@login_required
def manage_users():
    """
    Add users
    Delete users
    Reset user passwords
    """
    return render_template()