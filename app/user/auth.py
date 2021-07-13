from flask import request, redirect, url_for, flash, render_template
from flask_login import login_user, logout_user, current_user
from ..forms import LoginForm, RegisterForm
from ..db.helper import login_auth, add_user
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
                    flash(f"Login as {username}!", category="success")
                    return redirect(url_for("user.dashboard_page"))
                else:
                    flash("Wrong username or password.", category="alert")
                    return redirect(url_for("user.login_page"))
            else:
                for _, errors in form.errors.items():
                    for error in errors:
                        flash(error, category="alert")
                return redirect(url_for("user.login_page"))


@user_bp.route("/register", methods=["GET", "POST"])
def register_page():
    if current_user.is_active:
        flash("You have logined.", category="info")
        return redirect(url_for("user.dashboard_page"))
    else:
        form = RegisterForm()
        if request.method == "GET":
            return render_template("register.html", form=form)
        if request.method == "POST":
            if form.validate_on_submit():
                username = form.username.data
                password = form.password.data
                email = form.email.data
                if add_user(username, password, email, False):
                    flash("Register successfully.", category="success")
                    return redirect(url_for("user.login_page"))
                else:
                    flash("The username or the email has been used.", category="alert")
                    return redirect(url_for("user.register_page"))
            else:
                for _, errors in form.errors.items():
                    for error in errors:
                        flash(error, category="alert")
                return redirect(url_for("user.register_page"))


@user_bp.route("/logout", methods=["GET"])
def logout_page():
    logout_user()
    return redirect(url_for("main.index_page"))
