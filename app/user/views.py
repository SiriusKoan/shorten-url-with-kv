from flask import request, render_template, flash, redirect, url_for
from flask_login import current_user
from . import user_bp
from ..db.helper import render_user_record
from ..forms import DashboardFilterForm


@user_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard_page():
    form = DashboardFilterForm()
    if request.method == "GET":
        records = render_user_record(current_user.id)
        return render_template("dashboard.html", records=records, form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            print(form.start.data, form.end.data)
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    flash(error, category="alert")
        return redirect(url_for("user.dashboard_page"))


@user_bp.route("/setting", methods=["GET", "POST"])
def setting_page():
    if request.method == "GET":
        return ""
    if request.method == "POST":
        return ""
