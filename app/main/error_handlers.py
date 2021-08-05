from flask import render_template
from werkzeug.exceptions import HTTPException
from . import main_bp


@main_bp.app_errorhandler(HTTPException)
def handler(e):
    print(e)
    return render_template("error.html", code=e.code, name=e.name), e.code
