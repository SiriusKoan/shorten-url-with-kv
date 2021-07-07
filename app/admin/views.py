from flask import request
from . import admin_bp


@admin_bp.route("/admin_dashboard", methods=["GET", "POST"])
def dashboard_page():
    if request.method == "GET":
        pass
    if request.method == "POST":
        pass


@admin_bp.route("/manage_user", methods=["GET", "POST"])
def manage_user_page():
    if request.method == "GET":
        pass
    if request.method == "POST":
        pass
