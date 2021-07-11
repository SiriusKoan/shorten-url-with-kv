from . import db
from .models import Users, urls


def db_init():
    db.create_all()
    if not Users.query.filter_by(username="anonymous").first():
        user = Users("anonymous", "none", "none")
        db.session.add(user)
    if not Users.query.filter_by(username="admin"):
        admin = Users("admin", "admin", "admin@admin.com", True)
        db.session.add(admin)
    db.session.commit()


def get_redirect_url(new):
    if url := urls.query.filter_by(new=new).first():
        return url.old
    else:
        return False


def add_short_url(user_id, old, new):
    if urls.query.filter_by(new=new).first():
        return False
    else:
        url = urls(user_id, old, new)
        db.session.add(url)
        db.session.commit()
        return True
