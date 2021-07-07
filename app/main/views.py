from flask import request, render_template, redirect, url_for
from . import main_bp
from ..db import db


@main_bp.before_app_first_request
def db_init():
    db.create_all()


@main_bp.route("/", methods=["GET", "POST"])
def index_page():
    if request.method == "GET":
        return ""
        return render_template("index.html")
    if request.method == "POST":
        # TODO handle request
        return redirect(url_for("main.index_page"))


@main_bp.route("/<string:url>", methods=["GET"])
def redirect_page(url):
    return url
