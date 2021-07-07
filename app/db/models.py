import hashlib
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = "users"
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    verify_code = db.Column(db.String, unique=True, nullable=True)  # for futurn use
    api_key = db.Column(db.String, unique=True)
    urls = db.relationship("urls")
    register_time = db.Column(
        db.DateTime, default=datetime.datetime.now, nullable=False
    )

    @staticmethod
    def hash(s):
        return hashlib.sha256(s.encode("utf-8")).hexdigest()

    def __init__(self, username, password, email, is_admin=False) -> None:
        self.username = username
        self.password = hash(password)
        self.email = email
        self.is_admin = is_admin


class urls(db.Model):
    __tablename__ = "urls"
    ID = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.ID"), nullable=False)
    old = db.Column(db.String, nullable=False)
    new = db.Column(db.String, nullable=False, unique=True)
    use = db.Column(db.Integer, nullable=False, default=0)
    create_by = db.Column(db.String, nullable=False, default="web")  # web or api
    created_time = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)

    def __init__(self, user_id, old, new) -> None:
        self.user_id = user_id
        self.old = old
        self.new = new
