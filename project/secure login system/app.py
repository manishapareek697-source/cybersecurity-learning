
import os
import re
import hmac
import sqlite3
from pathlib import Path
from functools import wraps

from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash, g
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "users.db"

app = Flask(__name__)

# Set a persistent random secret in your environment before deployment.
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

if not app.secret_key:
    raise RuntimeError(
        "Set FLASK_SECRET_KEY before starting the app."
    )

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE") == "1",
    MAX_CONTENT_LENGTH=16 * 1024
)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DATABASE) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        """)


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("login"))
        return view(**kwargs)
    return wrapped_view


@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "same-origin"
    response.headers["Cache-Control"] = "no-store"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "form-action 'self'; frame-ancestors 'none'; "
        "base-uri 'self'"
    )
    return response


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not re.fullmatch(r"[A-Za-z0-9_]{3,30}", username):
            flash(
                "Username must be 3-30 characters: "
                "letters, numbers or underscores."
            )
            return render_template("register.html")

        if len(password) < 12 or len(password) > 128:
            flash("Password must be between 12 and 128 characters.")
            return render_template("register.html")

        db = get_db()

        existing = db.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if existing:
            flash("Username is already taken.")
            return render_template("register.html")

        password_hash = generate_password_hash(password)

        try:
            db.execute(
                "INSERT INTO users (username, password_hash) "
                "VALUES (?, ?)",
                (username, password_hash)
            )
            db.commit()
        except sqlite3.IntegrityError:
            flash("Username is already taken.")
            return render_template("register.html")

        flash("Account created. You can now log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = get_db().execute(
            "SELECT id, username, password_hash "
            "FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if user and check_password_hash(
            user["password_hash"], password
        ):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session.permanent = False

            return redirect(url_for("dashboard"))

        flash("Invalid username or password.")

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
