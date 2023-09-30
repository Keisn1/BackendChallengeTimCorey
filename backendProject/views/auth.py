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
        client_name = request.form["client_name"]
        client_email = request.form["client_email"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not client_name:
            error = "Client_name is required"
        if not client_email:
            error = "Email is required"
        elif not password:
            error = "Password is required"

        if error is None:
            try:
                db.execute(
                    "INSERT INTO clients (client_name, client_email, password) VALUES (?, ?, ?)",
                    (client_name, client_email, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Client with {client_email} is already registered"
            else:
                return redirect(
                    url_for("auth.login")
                )  # generates redirect response to the generated URL

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        client_email = request.form["client_email"]
        password = request.form["password"]
        db = get_db()
        error = None
        client = db.execute(
            "SELECT client_id, client_name, client_email, password FROM clients WHERE client_email = (?)",
            (client_email,),
        ).fetchone()

        if client == None:
            error = "Incorrect client_email"
        elif not check_password_hash(client["password"], password):
            error = "Incorred password"

        if error is None:
            session.clear()
            session["client_id"] = client["client_id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_client():
    # bp.before_app_request registers a function that is called before every
    # viewfunction no matter the URL is
    client_id = session.get("client_id")

    if client_id is None:
        g.client = None
    else:
        g.client = get_db.execute(
            "SELECT client_id, client_name, client_email FROM clients WHERE client_id = ?",
            (client_id),
        )


@bp.route("logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.client is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
