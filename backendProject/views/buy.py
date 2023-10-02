#!/usr/bin/env python3

from flask import (
    session,
    g,
    url_for,
    Blueprint,
    render_template,
    abort,
    request,
    flash,
    redirect,
)
from backendProject.db import get_db
from backendProject.views.auth import login_required

bp = Blueprint("buy", __name__)


@bp.route("/")
def index():
    db = get_db()
    purchases = db.execute(
        "SELECT c.client_id, c.client_name, p.amount, pr.product_id, pr.product_name, pr.description, p.created"
        " FROM purchase p JOIN clients c ON p.client_id = c.client_id"
        " JOIN product pr ON p.product_id = pr.product_id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template("buy/index.html", purchases=purchases)


@bp.route("/buy_product", methods=("POST", "GET"))
@login_required
def buy_product():
    products = get_db().execute("SELECT * FROM product;").fetchall()
    purchase_data = {}
    if request.method == "POST":
        for p in products:
            product_id = p["product_id"]
            amount = int(request.form[f"{product_id}"])
            if amount > 0:
                purchase_data[product_id] = amount
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            for product_id, amount in purchase_data.items():
                db.execute(
                    "INSERT INTO purchase (product_id, amount, client_id)"
                    " VALUES (?, ?, ?)",
                    (product_id, amount, g.user["client_id"]),
                )
            db.commit()
            return redirect(url_for("index"))

    return render_template("buy/buy_product.html", products=products)


@bp.route("/<int:id>/return_product", methods=("POST", "GET"))
@login_required
def return_product():
    return render_template("buy/return_product.html")
