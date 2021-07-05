from flask import request
from . import user_bp


@user_bp.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        pass
    if request.method == "POST":
        pass


@user_bp.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "GET":
        pass
    if request.method == "POST":
        pass


@user_bp.route("/logout", methods=["GET"])
def logout_page():
    pass
