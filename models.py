"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User (db.Model):
    """User."""

    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"<User id = {u.id} first_name= {u.first_name} last_name= {u.last_name} image_url= {u.image_url}>"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    image_url = db.Column(db.String, nullable=True)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

class Post (db.Model):
    """Post."""

    __tablename__ = "posts"

    def __repr__(self):
        p = self
        return f"<Post id = {p.id} titlee= {p.title} content= {p.content} created_at= {p.created_at} user_id={p.user_id}>"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
