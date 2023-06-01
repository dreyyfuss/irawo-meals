"""
App routes for the irawo-meals webapp
"""

from datetime import datetime, date, timedelta
from flask import flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os

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
        con = sqlite3.connect("irawo_meals/app.db")
        with con:
            # Set dictionary cursor to read database
            con.row_factory = sqlite3.Row
            db = con.cursor()

            # Unpack login form response
            username = request.form.get("username")
            password = request.form.get("password")
            
            # Get the user details from database
            db.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = db.fetchone()

            # Check if the login was valid
            if (user == None) or (not check_password_hash(user["password"], password)):
                flash("Incorrect username or password", "error")
                return render_template("login.html", username=username)

            # Get the groups to which the user belongs
            db.execute("SELECT group_id FROM users_groups WHERE user_id = ?", (user["id"],))
            groups = [i["group_id"] for i in db.fetchall()]

            # Initialize the session
            session["user_id"] = user["id"]
            if 1 in groups:
                session["is_admin"] = True
            else:
                session["is_admin"] = False
            if 2 in groups:
                session["is_management"] = True
            else:
                session["is_management"] = False
            if 3 in groups:
                session["is_professional"] = True
            else:
                session["is_professional"] = False

        return redirect("/")
    else:
        session.clear()
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
    allowance = 7
    current_date = date.today()

    if request.method == "POST":
        con = sqlite3.connect("irawo_meals/app.db")
        with con:
            # Set dictionary cursor to read database
            con.row_factory = sqlite3.Row
            db = con.cursor()

            # Unpack form response
            for i in range(1, allowance+1):
                meal_date = current_date + timedelta(days=i)
                lunch = request.form.get(f"lunch{meal_date}")
                dinner = request.form.get(f"dinner{meal_date}")
                breakfast = request.form.get(f"breakfast{meal_date}")

                print(lunch, dinner, breakfast)

                # Check if database record already exists
                db.execute(
                    "SELECT * FROM meals WHERE user_id = ? AND date = ?",
                    (session["user_id"], meal_date)
                )
                if not db.fetchone():
                    print("entered conditional")
                    # Add record to meals table
                    db.execute(
                        "INSERT INTO meals(date, user_id, breakfast, lunch, dinner) VALUES (?, ?, ?, ?, ?)",
                        (meal_date, session["user_id"], breakfast, lunch, dinner)
                    )
                    db.execute(
                        "SELECT * FROM meals WHERE user_id = ? AND date = ?",
                        (session["user_id"], meal_date)
                    )
                else:
                    # Update the record in meals table
                    print("entered else")
                    db.execute(
                        """UPDATE meals SET (breakfast, lunch, dinner) = (?, ?, ?)
                        WHERE user_id = ? and date = ?""",
                        (breakfast, lunch, dinner, session["user_id"], meal_date)
                    )

        return redirect("/")

    else:
        week = [current_date + timedelta(days=i) for i in range(1, allowance+1)]

        con = sqlite3.connect("irawo_meals/app.db")
        with con:
            # Set dictionary cursor to read database
            con.row_factory = sqlite3.Row
            db = con.cursor()

            # Get current username
            db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],))
            username = db.fetchone()["username"]

            # Get already ticked meals
            db.execute(
                "SELECT * FROM meals WHERE user_id = ? AND date > ? ORDER BY date ASC LIMIT ?", 
                (session["user_id"], current_date, allowance)
            )
            meals = db.fetchall()
            # Ensure the length of the meals list is up to the allowance
            while len(meals) < allowance:
                meals.append(None)

        return render_template("index.html", week=week, username=username, meals=meals)


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """
    Display meal ticking history for user between selected dates
    """
    if request.method == "POST":
        con = sqlite3.connect("irawo_meals/app.db")
        with con:
            # Set dictionary cursor to read database
            con.row_factory = sqlite3.Row
            db = con.cursor()

            # Unpack form responses
            username = request.form.get("username")
            user_id = request.form.get("user_id")
            start_date = request.form.get("start_date")
            end_date = request.form.get("end_date")

            # Get meals within required date
            db.execute(
                "SELECT * FROM meals WHERE date >= ? AND date <= ? AND user_id = ?",
                (start_date, end_date, user_id)
            )
            records = db.fetchall()

            return render_template(
                "history.html", start_date=start_date, end_date=end_date,
                records=records, user_id=user_id, username=username
            )

    else:
        con = sqlite3.connect("irawo_meals/app.db")
        with con:
            # Set dictionary cursor to read database
            con.row_factory = sqlite3.Row
            db = con.cursor()

            # Get name of current user
            db.execute("SELECT username FROM users WHERE id = ?", (session["user_id"],))
            username = db.fetchone()["username"]

        return render_template("history.html", user_id=session["user_id"], username=username)


@app.route("/account", methods=["GET"])
@login_required
def account():
    """
    Allows user to manage account (change username & password)
    """
    con = sqlite3.connect("irawo_meals/app.db")
    with con:
        # Set dictionary cursor to read database
        con.row_factory = sqlite3.Row
        db = con.cursor()

        # Get current username
        db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],))
        username = db.fetchone()["username"]

    return render_template("account.html", current_username=username)


@app.route("/account/username", methods=["POST"])
@login_required
def change_username():
    """
    Change username of current user
    """
    con = sqlite3.connect("irawo_meals/app.db")
    with con:
        # Set dictionary cursor to read database
        con.row_factory = sqlite3.Row
        db = con.cursor()

        # Unpack form response
        new_username = request.form.get("username")

        # Check if username is already taken
        db.execute("SELECT username FROM users")
        usernames = [record["username"] for record in db.fetchall()]

        if new_username in usernames:
            flash("That username is already taken", "warning")
            return redirect("/account")
        else:
            # Change username in database
            db.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, session["user_id"]))

    return redirect("/")


@app.route("/account/password", methods=["POST"])
@login_required
def change_password():
    """
    Change password of current user
    """
    con = sqlite3.connect("irawo_meals/app.db")
    with con:
        # Set dictionary cursor to read database
        con.row_factory = sqlite3.Row
        db = con.cursor()

        # Get current password hash
        db.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],))
        current_hash = db.fetchone()["password"]

        # Unpack form response
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # Check if current password is correct
        if not check_password_hash(current_hash, current_password):
            flash("Incorrect current password")
            return redirect("/account")

        # Check if new password matches confirmation
        if not (new_password == confirmation):
            flash("New password and confirmation do not match")
            return redirect("/account")

        # Add new password hash to database
        new_hash = generate_password_hash(new_password)
        db.execute("UPDATE users SET password = ? WHERE id = ?", (new_hash, session["user_id"]))

    return redirect("/login")


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
        con = sqlite3.connect("irawo_meals/app.db")
        with con:
            # Set dictionary cursor to read database
            con.row_factory = sqlite3.Row
            db = con.cursor()

            # Get current date
            current_date = date.today()

            # Get all the meals on that day
            db.execute("SELECT * FROM meals WHERE date = ?", (current_date + timedelta(days=1),))
            meals = db.fetchall()

            # Count each meal type
            count = {
                "Normal Lunch":0,
                "Late Lunch":0,
                "Packed Lunch":0,
                "Normal Dinner":0,
                "Late Dinner":0,
                "Normal Breakfast":0,
                "Packed Breakfast":0
            }

            for meal in meals:

                # Count lunch type
                if meal["lunch"] == "normal":
                    count["Normal Lunch"] += 1
                elif meal["lunch"] == "late":
                    count["Late Lunch"] += 1
                elif meal["lunch"] == "packed":
                    count["Packed Lunch"] += 1

                # Count dinner type
                if meal["dinner"] == "normal":
                    count["Normal Dinner"] += 1
                if meal["dinner"] == "late":
                    count["Late Dinner"] += 1

                # Count breakfast type
                if meal["breakfast"] == "normal":
                    count["Normal Breakfast"] += 1
                if meal["breakfast"] == "packed":
                    count["Packed Breakfast"] += 1
            

        return render_template("meal_count.html", meal_count=count)


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
    con = sqlite3.connect("irawo_meals/app.db")
    with con:
        # Set dictionary cursor to read database
        con.row_factory = sqlite3.Row
        db = con.cursor()

        if request.method == "POST":
            return redirect("/manage_users")

        else:
            # Get list of all users
            db.execute("SELECT * FROM users WHERE id > 1")
            users = db.fetchall()

            return render_template("manage_users.html", users=users)


@app.route("/users/history", methods=["POST"])
@login_required
def user_history():
    """
    Display meal ticking history for user between selected dates
    """
    if request.method == "POST":
        con = sqlite3.connect("irawo_meals/app.db")
        with con:
            # Set dictionary cursor to read database
            con.row_factory = sqlite3.Row
            db = con.cursor()

            # Unpack form response
            user_id = request.form.get("user_id")

            # Get name of user
            db.execute("SELECT username FROM users WHERE id = ?", (user_id,))
            username = db.fetchone()["username"]

            return render_template("history.html", user_id=user_id, username=username)


@app.route("/users/reset", methods=["POST"])
@login_required
@admin_required
def reset_password():
    con = sqlite3.connect("irawo_meals/app.db")
    with con:
        # Set dictionary cursor to read database
        db = con.cursor()

        # Get user to reset password
        user_id = request.form.get("user_id")

        # Reset user password in database
        new_hash = generate_password_hash("")
        db.execute("UPDATE users SET password = ? WHERE id = ?", (new_hash, user_id))

    return redirect("/users/manage")


@app.route("/users/delete", methods=["POST"])
@login_required
@admin_required
def delete_user():
    con = sqlite3.connect("irawo_meals/app.db")
    with con:
        # Set dictionary cursor to read database
        db = con.cursor()

        # Get user to delete from form
        user_id = request.form.get("user_id")

        # Delete user from database
        db.execute("DELETE FROM users_groups WHERE user_id = ?", (user_id,))
        db.execute("DELETE FROM meals WHERE user_id = ?", (user_id,))
        db.execute("DELETE FROM users WHERE id = ?", (user_id,))

    return redirect("/users/manage")


@app.route("/users/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_users():
    """
    Add new users
    """
    if request.method == "POST":
        con = sqlite3.connect("irawo_meals/app.db")
        with con:
            # Set dictionary cursor to read database
            con.row_factory = sqlite3.Row
            db = con.cursor()
            
            # Unpack form response
            username = request.form.get("username")
            password = generate_password_hash(request.form.get("password"))
            admin = request.form.get("admin")
            management = request.form.get("management")
            professional = request.form.get("professional")

            # Check if user exists
            db.execute("SELECT username FROM users")
            usernames = [record["username"] for record in db.fetchall()]
            if username in usernames:
                flash("That username is already taken", "warning")
                return redirect("/users/add")
            else:
                # Add new user to users table
                db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                db.execute("SELECT * FROM users WHERE username = ?", (username,))
                new_user = db.fetchone()
                # Add user to appropriate groups
                if admin == "on":
                    db.execute(
                        "INSERT INTO users_groups(user_id, group_id) VALUES(?, 1)",
                        (new_user["id"],)
                    )
                if management == "on":
                    db.execute(
                        "INSERT INTO users_groups(user_id, group_id) VALUES(?, 2)",
                        (new_user["id"],)
                    )
                if professional == "on":
                    db.execute(
                        "INSERT INTO users_groups(user_id, group_id) VALUES(?, 3)",
                        (new_user["id"],)
                    )

            return redirect("/users/manage")
    
    else:
        return render_template("add_users.html")