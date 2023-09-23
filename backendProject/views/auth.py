#!/usr/bin/env python3

import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from werkzeug.security import check_password_hash, generate_password_hash

from backendProject.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")
# needs to know where it is defined, therefore __name__
# the url prefix is prepended to all the URLs associated with the blueprint
# the blueprint is called 'auth'


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        user_email = request.form["user_email"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required"
        if not user_email:
            error = "Email is required"
        elif not password:
            error = "Password is required"

        if error is None:
            try:
                db.execute(
                    "INSERT INTO purchase (username, user_email, password) VALUES (?, ?)",
                    (username, user_email, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User with {user_email} is already registered"
            else:
                return redirect(
                    url_for("auth.login")
                )  # generates redirect response to the generated URL

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_email = request.form["user_email"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT username, user_email, password FROM user WHERE user_email = ?",
            (user_email),
        ).fetchone()

        if user == None:
            error = "Incorrect user_email"
        elif not check_password_hash(password, user["password"]):
            erro = "Incorred password"

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    # bp.before_app_request registers a function that is called before every
    # viewfunction no matter the URL is
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db.execute(
            "SELECT user_id, username, user_email FROM user WHERE user_id = ?",
            (user_id),
        )


@bp.route("logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
