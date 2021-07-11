from . import main_bp


@main_bp.app_errorhandler(404)
def not_found_handler(e):
    return "", 404


@main_bp.app_errorhandler(401)
def unauthorized_handler(e):
    return "", 401


@main_bp.app_errorhandler(403)
def forbidden_handler(e):
    return "", 403
