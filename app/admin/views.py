from flask import request
from . import admin_bp


@admin_bp.route("/admin_dashboard", methods=["GET", "POST"])
def dashboard_page():
    if request.method == "GET":
        return ""
    if request.method == "POST":
        return ""


@admin_bp.route("/manage_user", methods=["GET", "POST"])
def manage_user_page():
    if request.method == "GET":
        return ""
    if request.method == "POST":
        # add user
        return ""


@admin_bp.route("/manage_user_backend", methods=["PATCH", "DELETE"])
def manage_user_backend():
    if request.method == "PATCH":
        return ""
    if request.method == "DELETE":
        return ""
