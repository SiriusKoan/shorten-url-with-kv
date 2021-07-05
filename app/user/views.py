from flask import request
from . import user_bp


@user_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard_page():
    if request.method == "GET":
        pass
    if request.method == "POST":
        pass
