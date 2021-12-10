import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp # Don't know what this is for
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import error, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///movies.db")


@app.route("/")
@login_required
def index():
    """Show watched movie list"""

    # Get user id from session
    user_id = session["user_id"]

    # Query database for user's movie list
    movies = db.execute("SELECT * FROM movie WHERE user_id = ?", user_id)

    # Initialize total of movies watched
    total_movies = 0

    # Increment user's total of movies watched
    for movie in movies:
        total_movies += 1

    # Render template
    return render_template("index.html", movies=movies, total_movies=total_movies)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return error("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("Must provide password", 403)

        # Query database for user info
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return error("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Remember user's nickname
        session["nickname"] = rows[0]["nickname"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return error("Must provide username", 400)

        # Ensure nickname was submitted
        if not request.form.get("nickname"):
            return error("Must provide nickname", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("Missing password", 400)

        # Ensure password length is longer than 6 characters
        elif len(request.form.get("password")) < 6:
            return error("Password must be longer than 6 characters")

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return error("Missing confirmation password", 400)


        # Query database for username
        username_exists = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username does not already exist
        if len(username_exists) == 1:
            return error("Username is unavailable", 400)

        # Query database for nickname
        nickname_exists = db.execute("SELECT * FROM users WHERE nickname = ?", request.form.get("nickname"))

        # Ensure nickname does not already exist
        if len(nickname_exists) == 1:
            return error("Nickname is unavailable", 400)

        # Ensure password and password confirmation are the same
        elif request.form.get("password") != request.form.get("confirmation"):
            return error("Passwords don't match", 400)

        else:
            # Hash password
            password = generate_password_hash(request.form.get("password"))

            # Register new user into database
            db.execute("INSERT INTO users (username, nickname, hash) VALUES (?, ?, ?)",
                        request.form.get("username"), request.form.get("nickname"), password)

            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]

            # Remember user's nickname
            session["nickname"] = rows[0]["nickname"]

            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    """Select Edit Item"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # If edit nickname was selected
        if request.form.get("editNickname"):
            return render_template("editNickname.html")

        # If edit password was selected
        if request.form.get("editPassword"):
            return render_template("editPassword.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("edit.html")


@app.route("/editNickname", methods=["GET", "POST"])
@login_required
def editNickname():
    """Edit Nickname"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get user id from session
        user_id = session["user_id"]

        # Initialize edit value
        edit_value = "nickname"

        # Ensure nickname was submitted
        if not request.form.get("nickname"):
            return error("Missing nickname", 400)

        # Query database for user info
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        # Ensure new nickname is not the same as current nickname
        if rows[0]["nickname"] == request.form.get("nickname"):
            return error("New nickname required", 403)

        else:
            # Store new nickname to users database
            db.execute("UPDATE users SET nickname = ? WHERE id = ?", request.form.get("nickname"), user_id)

            # Edit user's nickname in session
            session["nickname"] = request.form.get("nickname")

            # Render template
            return render_template("edited.html", edit_value=edit_value)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("editNickname.html")


@app.route("/editPassword", methods=["GET", "POST"])
@login_required
def editPassword():
    """Edit password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get user id from session
        user_id = session["user_id"]

        # Initialize edit value
        edit_value = "password"

        # Ensure password was submitted
        if not request.form.get("password"):
            return error("Missing test password", 400)

        # Ensure new password was submitted
        elif not request.form.get("new_password"):
            return error("Missing new password", 400)

        # Ensure new password confirmation was submitted
        elif not request.form.get("new_confirmation"):
            return error("Missing confirmation password", 400)

        # Ensure new password and new password confirmation are the same
        elif request.form.get("new_password") != request.form.get("new_confirmation"):
            return error("Passwords don't match", 403)

        # Query database for user info
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)

        # Enusre current password is correct
        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return error("Invalid current password", 403)

        # Ensure new password is not the same as current password
        if check_password_hash(rows[0]["hash"], request.form.get("new_password")):
            return error("New password required", 403)

        else:
            # Hash new password
            new_password = generate_password_hash(request.form.get("new_password"))

            # Store new password to users database
            db.execute("UPDATE users SET hash = ? WHERE id = ?", new_password, user_id)

            # Render template
            return render_template("edited.html", edit_value=edit_value)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("editPassword.html")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add movie"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get user id from session
        user_id = session["user_id"]

        # Ensure date was submitted
        if not request.form.get("date"):
            flash("Please provide a date", "error")
            return redirect(request.url)

        # Ensure title was submitted
        elif not request.form.get("title"):
            flash("Please provide a title", "error")
            return redirect(request.url)

        # Add movie to movies database
        else:
            db.execute("INSERT INTO movie (user_id, date, title, director, codirector, year, rating) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        user_id, request.form.get("date"), request.form.get("title"), request.form.get("director"), request.form.get("codirector"), request.form.get("year"), request.form.get("rating"))

            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("add.html")


@app.route("/deleteSearch", methods=["GET", "POST"])
@login_required
def deleteSearch():
    """Search movie to delete"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get user id from session
        user_id = session["user_id"]

        # If List All Movies was selected
        if request.form['action'] == 'list-movies':
            results = db.execute("SELECT * FROM movie WHERE user_id = ?", user_id)

            empty_result = len(results) == 0
            # Render template
            return render_template("delete.html", results=results, empty_result=empty_result)


        # Ensure search category was selected
        if not request.form.get("select"):
            flash("Please provide a search category", "error")
            return redirect(request.url)

        # Ensure search item was submitted
        elif not request.form.get("search"):
            flash("Please provide a search item", "error")
            return redirect(request.url)

        # Get searched item
        else:
            selected = request.form.get("select")
            searched = request.form.get("search")

            # Initialize results
            results = None

            # If title was selected
            if selected == "title":
                results = db.execute("SELECT * FROM movie WHERE user_id = ? AND title LIKE ?", user_id, "%" + searched + "%")

            # If directors was selected
            elif selected == "directors":
                results = db.execute("SELECT * FROM movie WHERE user_id = ? AND (director LIKE ? OR codirector LIKE ?)", user_id, "%" + searched + "%", "%" + searched + "%")

            # If year was selected
            elif selected == "year":
                results = db.execute("SELECT * FROM movie WHERE user_id = ? AND year LIKE ?", user_id, "%" + searched + "%")

            # If searched item does not exist
            empty_result = len(results) == 0

            # Render template
            return render_template("delete.html", results=results, empty_result=empty_result)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("deleteSearch.html")


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    """Delete movie"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get user id from session
        user_id = session["user_id"]

        # Get movie ids user checked
        movies_list = request.form.getlist("movie_id") # returns list with strings

        # Initialize total movies deleted
        total_movies = 0

        # Delete checked movies and increment total movies deleted
        for movie in range(len(movies_list)):
            db.execute("DELETE FROM movie WHERE movie_id = ?", movies_list[movie])
            total_movies += 1

        # Render template
        return render_template("deleted.html", total_movies=total_movies)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("deleted.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return error(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)