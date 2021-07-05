from . import main_bp


@main_bp.app_errorhandler(404)
def not_found_handler(e):
    pass


@main_bp.app_errorhandler(401)
def unauthorized_handler(e):
    pass


@main_bp.app_errorhandler(403)
def forbidden_handler(e):
    pass
