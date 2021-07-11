from flask import request, render_template, redirect, url_for, flash, abort
from flask_login import current_user
from . import main_bp
from ..db.helper import add_short_url, db_init, get_redirect_url
from ..forms import ShortUrlForm


@main_bp.before_app_first_request
def database_init():
    db_init()


@main_bp.route("/", methods=["GET", "POST"])
def index_page():
    form = ShortUrlForm()
    if request.method == "GET":
        return render_template("index.html", form=form)
    if request.method == "POST":
        if form.validate_on_submit():
            old = form.old.data
            new = form.new.data
            user_id = current_user.id if current_user.is_active else 1
            if add_short_url(user_id, old, new):
                flash("Successfully add this record.", category="success")
            else:
                flash("The url has been used.", category="alert")
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    flash(error, category="alert")

        return redirect(url_for("main.index_page"))


@main_bp.route("/<string:url>", methods=["GET"])
def redirect_page(url):
    if old := get_redirect_url(url):
        return redirect(old)
    else:
        abort(404)
