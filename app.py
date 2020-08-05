"""Blogly application."""
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template, flash, session
from models import db, connect_db, User, Post
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


@app.route("/", methods=['GET'])
def rd():
    """redirect to user page"""
    return redirect("/users")


@app.route("/users", methods=['GET'])
def list_users():
    """List users and show add form."""
    users = User.query.all()
    return render_template("list.html", users=users)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Show a form to create a new user"""

    return render_template('add-user.html')


@app.route("/users/new", methods=["POST"])
def users_new():
    """Handle form submission for creating a new user"""

    new_user = User(
        first_name=request.form['first_name'] or None,
        last_name=request.form['last_name'],
        image_url=request.form['image_url'])

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


# @app.route("/display-user-added", methods=['GET', 'POST'])
# def display_user(first_name):
#     users = User.query.all()
#     user = User.query.get_or_404(first_name)
#     return render_template("/display-user-added.html", users=users, user=user)

@app.route("/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""
    user = User.query.get_or_404(user_id)
    posts = Post.filter_by(user_id)
    return render_template("detail.html", user=user, posts = posts)


@app.route("/<int:user_id>/edit")
def show_editpage(user_id):
    """Show info on a single user."""
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.route('/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/<int:user_id>/delete")
def delete(user_id):
    """Show info on a single user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(f"/users")

@app.route("/<int:user_id>/posts/new", methods=["GET"])
def show_form(user_id):
    """show form for adding post"""
    user = User.query.get_or_404(user_id)
    return render_template("new-post.html", user=user)

@app.route("/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Handle add form; add post and redirect to the user detail page"""
    user = User.query.get_or_404(user_id)
    post = Post(
        title=request.form['title'] or None,
        content=request.form['content'],
        user_id=user_id)
       
    db.session.add(post)
    db.session.commit()

    return render_template("detail.html", user=user)


@app.route("/<int:post_id>")
def show_post():
    """Show a post. Show buttons to edit and delete the post."""
    
    return render_template("post.html")


@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """Show info on a single user."""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/posts")

@app.route("/posts/<int:post_id>/edit")
def edit():
        """Show form to edit a post, and to cancel (back to user page)."""
        return render_template("edit-post.html")

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_form():
    """Handle editing of a post. Redirect back to the post view."""
    post = Post.query.get_or_404(post_id)
    title = request.form('title')
    content = request.form('content')
    db.session.add(post)
    db.session.add(title)
    db.session.add(content)
    db.session.commit()
    return redirect("/posts")
