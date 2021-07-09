from flask import request
from flask_login import login_user
from app.user_helper import User
from . import user_bp


@user_bp.route("/login", methods=["GET", "POST"])
def login_page():
    user = User()
    user.id = 1
    login_user(user)
    return ""
    if request.method == "GET":
        pass
    if request.method == "POST":
        pass


@user_bp.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "GET":
        return ""
    if request.method == "POST":
        return ""


@user_bp.route("/logout", methods=["GET"])
def logout_page():
    return ""
