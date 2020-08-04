"""Blogly application."""
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template, flash, session
from models import db, connect_db, User
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


@app.route("/")
def list_users():
    """List users and show add form."""

    users = User.query.all()
    user = User.query.get_or_404(user_id)
    return render_template("list.html", users=users)


@app.route("/add-user")
def add_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    users = User.query.all()
    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()
    return render_template("add-user.html", users=users)


# @app.route("/display-user-added", methods=['GET', 'POST'])
# def display_user(first_name):
#     users = User.query.all()
#     user = User.query.get_or_404(first_name)
#     return render_template("/display-user-added.html", users=users, user=user)

@app.route("/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""
    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)
