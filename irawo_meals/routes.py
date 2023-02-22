"""
App routes for the irawo-meals webapp
"""

from datetime import datetime, date, timedelta
from flask import flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

from irawo_meals import app
from irawo_meals.helpers import admin_required, format_weekday, login_required, management_required


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
    if request.method == "POST":
        session["user_id"] = 1
        session["is_professional"] = True
        session["is_admin"] = True
        session["is_management"] = True
        return redirect("/")
    
    else:
        return render_template("login.html")


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
    if request.method == "POST":
        return redirect("/")

    else:
        current_date = date.today()
        week = [current_date + timedelta(days=i) for i in range(1, 8)]

        return render_template("index.html", week=week)


@app.route("/personal_history", methods=["GET", "POST"])
@login_required
def personal_history():
    """
    Display meal ticking history for user between selected dates
    """
    if request.method == "POST":
        return redirect("/personal_history")

    else:
        records = [{"Date":date.today(), "Lunch":"Late", "Dinner":"Normal", "Breakfast":"Packed"},
                    {"Date":date.today(), "Lunch":"Late", "Dinner":"Normal", "Breakfast":"Packed"}]
        return render_template("personal_history.html", records=records)


@app.route("/account")
@login_required
def account():
    """
    Allows user to manage account (change username & password)
    """
    if request.method == "POST":
        return redirect("/account")

    else:
        return render_template("account.html")


@app.route("/meal_count")
@login_required
@management_required
def meal_count():
    """
    Shows meal count for the day
    """
    if request.method == "POST":
        return redirect("/meal_count")

    else:
        pb = 4
        nb = 9
        pl = 2
        nl = 6
        ll = 3
        nd = 12
        ld = 2
        meals = {"Packed Breakfast":pb, "Normal Breakfast":nb, "Packed Lunch":pl,
                "Normal Lunch":nl, "Late Lunch":ll, "Normal Dinner":nd, "Late Dinner":ld}
        return render_template("meal_count.html", meals=meals)


@app.route("/general_history", methods=["GET", "POST"])
@login_required
@management_required
def general_history():
    """
    Display ticking history for all active users between two dates
    """
    if request.method == "POST":
        return redirect("/general_history")

    else:
        return render_template("general_history.html")


@app.route("/users", methods=["GET", "POST"])
@login_required
@admin_required
def users():
    """
    Select between add users and manage users
    """
    if request.method == "GET":
        return render_template("users.html")


@app.route("/users/manage", methods=["GET", "POST"])
@login_required
@admin_required
def manage_users():
    """
    Delete users
    Reset user passwords
    """
    if request.method == "POST":
        return redirect("/manage_users")

    else:
        users = ["Anthony Alikah", "Ibukun Afolami", "John Onyejegbu"]
        return render_template("manage_users.html", users=users)

@app.route("/users/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_users():
    """
    Add new users
    """
    if request.method == "POST":
        return redirect("/users/manage")
    
    else:
        return render_template("add_users.html")