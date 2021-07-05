from flask import request, render_template, redirect, url_for
from . import main_bp


@main_bp.route("/", methods=["GET", "POST"])
def index_page():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        # TODO handle request
        return redirect(url_for("main.index_page"))
