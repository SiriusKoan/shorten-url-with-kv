from . import db
from .models import Users, urls
from ..user_helper import User


def db_init():
    db.create_all()
    if not Users.query.filter_by(username="anonymous").first():
        user = Users("anonymous", "none", "none")
        db.session.add(user)
    if not Users.query.filter_by(username="admin").first():
        admin = Users("admin", "admin", "admin@admin.com", True)
        db.session.add(admin)
    db.session.commit()


def get_redirect_url(new):
    if url := urls.query.filter_by(new=new).first():
        return url.old
    else:
        return False


def add_use(url):
    url = urls.query.filter_by(new=url).first()
    url.use += 1
    db.session.commit()


def add_short_url(user_id, old, new):
    if urls.query.filter_by(new=new).first():
        return False
    else:
        url = urls(user_id, old, new)
        db.session.add(url)
        db.session.commit()
        return True


def login_auth(username, password):
    if user := Users.query.filter_by(username=username).first():
        if user.check_password(password):
            sessionUser = User()
            sessionUser.id = user.id
            return sessionUser
    return False


def add_user(username, password, email, is_admin=False):
    if (not Users.query.filter_by(username=username).first()) and (
        not Users.query.filter_by(email=email).first()
    ):
        user = Users(username, password, email, is_admin)
        db.session.add(user)
        db.session.commit()
        return True
    return False


def url_to_dict(url_objects: list):
    li = []
    for url in url_objects:
        d = dict()
        d["user_id"] = url.user_id
        d["old"] = url.old
        d["new"] = url.new
        d["use"] = url.use
        d["create_by"] = url.create_by
        d["created_time"] = url.created_time.strftime("%Y-%m-%d %H:%M:%S")
        li.append(d)
    return li


def user_to_dict(user_objects: list):
    li = []
    for user in user_objects:
        d = dict()
        d["id"] = user.id
        d["username"] = user.username
        d["email"] = user.email
        d["is_admin"] = user.is_admin
        d["verify_code"] = user.verify_code
        d["api_key"] = user.api_key
        d["register_time"] = user.register_time
        li.append(d)
    return li


def render_user_record(filter=None):
    records = urls.query
    if filter:
        user_id = filter.get("user_id", None)
        if user_id:
            records = records.filter_by(user_id=user_id)

        time = filter.get("time", None)
        if time:
            time = time.split(";")
            start, end = time[0], time[1]
            records = records.filter(urls.created_time >= start).filter(
                urls.created_time <= end
            )
    records = url_to_dict(records.all())
    return records
