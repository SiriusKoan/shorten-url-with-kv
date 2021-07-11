from flask import request, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, current_user
from ..forms import LoginForm
from ..db.helper import login_auth
from . import user_bp


@user_bp.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_active:
        flash("You have logined.", category="info")
        return redirect(url_for("user.dashboard_page"))
    else:
        form = LoginForm()
        if request.method == "GET":
            return render_template("login.html", form=form)
        if request.method == "POST":
            if form.validate_on_submit():
                username = form.username.data
                password = form.password.data
                if user := login_auth(username, password):
                    login_user(user)
                    return redirect(url_for("user.dashboard_page"))
                else:
                    flash("Login failed.", category="alert")
                    return redirect(url_for("user.login_page"))
            else:
                flash("Invalid.")
                return redirect(url_for("user.login_page"))


@user_bp.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "GET":
        return ""
    if request.method == "POST":
        return ""


@user_bp.route("/logout", methods=["GET"])
def logout_page():
    logout_user()
    return redirect(url_for("main.index_page"))
