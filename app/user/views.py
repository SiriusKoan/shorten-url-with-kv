import datetime
from flask import request, render_template, flash, redirect, url_for, make_response
from flask_login import current_user, login_required
from . import user_bp
from ..db.helper import (
    render_user_record,
    render_user_data,
    update_user_data,
    check_email_duplicate,
)
from ..forms import DashboardFilterForm, UserSettingForm


@user_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard_page():
    filter = dict()
    if time := request.cookies.get("time"):
        filter["time"] = time
        time = time.split(";")
        start = datetime.datetime.strptime(time[0], "%Y-%m-%d")
        end = datetime.datetime.strptime(time[1], "%Y-%m-%d") - datetime.timedelta(
            days=1
        )
        form = DashboardFilterForm(start=start, end=end)
    else:
        form = DashboardFilterForm()
    filter["user_id"] = current_user.id
    if request.method == "GET":
        records = render_user_record(filter=filter)
        return render_template("dashboard.html", records=records, form=form)
    if request.method == "POST":
        response = make_response(redirect(url_for("user.dashboard_page")))
        if form.validate_on_submit():
            cookies = []
            start = form.start.data.strftime("%Y-%m-%d")
            end = (form.end.data + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            cookies.append(("time", ";".join([start, end])))
            response.delete_cookie("time")
            for cookie in cookies:
                response.set_cookie(*cookie)
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    flash(error, category="alert")
        return response


@user_bp.route("/setting", methods=["GET", "POST"])
@login_required
def setting_page():
    data = render_user_data(current_user.id)
    form = UserSettingForm(email=data["email"])
    if request.method == "GET":
        return render_template("user_setting.html", data=data, form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            password = form.password.data
            email = form.email.data
            if check_email_duplicate(current_user.id, email):
                if update_user_data(current_user.id, password, email):
                    flash("OK.", category="success")
                else:
                    flash("Unknown error.", category="alert")
            else:
                flash("The email has been used.", category="alert")
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    flash(error, category="alert")
        return redirect(url_for("user.setting_page"))
