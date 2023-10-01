#!/usr/bin/env python3

from flask import session, g, url_for, Blueprint, render_template
from backendProject.db import get_db

bp = Blueprint("buy", __name__)


@bp.route("/")
def index():
    db = get_db()
    purchases = db.execute(
        "SELECT p.id, p.client_id, p.product_id, pr.product_name, created"
        " FROM purchase p JOIN clients c ON p.client_id = c.client_id"
        " JOIN product pr ON p.product_id = pr.product_id"
        " ORDER BY created DESC"
    ).fetchall()
    print(purchases)
    return render_template("buy/index.html", purchases=purchases)
