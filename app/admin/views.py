import datetime
from flask import request, make_response, redirect, url_for, render_template, flash
from flask_login import login_required
from . import admin_bp
from ..db.helper import add_user, render_user_record, render_users_data, delete_user, update_user_data
from ..forms import AdminDashboardFilter, AddUserForm
from ..user_helper import admin_required


@admin_bp.route("/admin_dashboard", methods=["GET", "POST"])
@admin_required
@login_required
def dashboard_page():
    filter = dict()
    form_args = dict()
    if time := request.cookies.get("time"):
        filter["time"] = time
        time = time.split(";")
        start = datetime.datetime.strptime(time[0], "%Y-%m-%d")
        end = datetime.datetime.strptime(time[1], "%Y-%m-%d") - datetime.timedelta(
            days=1
        )
        form_args["start"] = start
        form_args["end"] = end
    if user_id := request.cookies.get("user_id"):
        filter["user_id"] = user_id
        form_args["user_id"] = user_id
    form = AdminDashboardFilter(**form_args)
    if request.method == "GET":
        records = render_user_record(filter=filter)
        return render_template("admin_dashboard.html", records=records, form=form)
    if request.method == "POST":
        response = make_response(redirect(url_for("admin.dashboard_page")))
        if form.validate_on_submit():
            cookies = []
            if form.start.data and form.end.data:
                start = form.start.data.strftime("%Y-%m-%d")
                end = (form.end.data + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
                cookies.append(("time", ";".join([start, end])))
            if form.user_id.data:
                user_id = form.user_id.data
                cookies.append(("user_id", str(user_id)))
            response.delete_cookie("time")
            response.delete_cookie("user_id")
            for cookie in cookies:
                response.set_cookie(*cookie)
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    flash(error, category="alert")
        return response


@admin_bp.route("/manage_user", methods=["GET", "POST"])
@admin_required
@login_required
def manage_user_page():
    form = AddUserForm()
    if request.method == "GET":
        data = render_users_data()
        return render_template("manage_user.html", form=form, data=data)
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            email = form.email.data
            is_admin = form.is_admin.data
            if add_user(username, password, email, is_admin):
                flash("Add user successfully.", category="success")
            else:
                flash("The username or the email has been used.", category="alert")
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    flash(error, category="alert")
        return redirect(url_for("admin.manage_user_page"))


@admin_bp.route("/manage_user_backend", methods=["PATCH", "DELETE"])
@admin_required
@login_required
def manage_user_backend():
    if request.method == "PATCH":
        data = request.get_json(force=True)
        user_id = data.pop("user_id")
        if (msg := update_user_data(user_id, **data)) == True:
            return "T;OK."
        else:
            return "F;" + msg, 400
    if request.method == "DELETE":
        data = request.get_json(force=True)
        user_id = data["user_id"]
        if (msg := delete_user(user_id)) == True:
            return "T;OK."
        else:
            return "F;" + msg, 400

