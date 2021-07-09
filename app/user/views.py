from flask import request
from . import user_bp


@user_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard_page():
    if request.method == "GET":
        return ""
    if request.method == "POST":
        return ""


@user_bp.route("/setting", methods=["GET", "POST"])
def setting_page():
    if request.method == "GET":
        return ""
    if request.method == "POST":
        return ""
