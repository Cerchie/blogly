"""Blogly application."""
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template, flash, session
from models import db, connect_db, User, Post, Tag, PostTag
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.drop_all()
db.create_all()


#________________________________________-
# USER ROUTES
#_________________________________________
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
    posts = Post.query.filter(user.id == user_id).all()
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
    tags = Tag.query.all()
    user = User.query.get_or_404(user_id)
    return render_template("new-post.html", user=user)

#________________________________________-
# POST ROUTES
#_________________________________________

@app.route('/<int:user_id>/posts/new', methods=["POST"])
def posts_new(user_id):
    """Handle form submission for creating a new post for a specific user"""

    user = User.query.get_or_404(user_id)
    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user)

    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show a post. Show buttons to edit and delete the post."""
    tags = Tag.query.all()
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """delete post."""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/users")

@app.route("/posts/<int:post_id>/edit")
def edit(post_id):
        post = Post.query.get_or_404(post_id)
        """Show form to edit a post, and to cancel (back to user page)."""
        tags = Tag.query.all()
        return render_template("edit-post.html", post_id=post_id, tags = tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_form(post_id):
    """Handle editing of a post. Redirect back to the post view."""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()
    return redirect("/users")
#________________________________________-
# TAG ROUTES
#_________________________________________

@app.route("/tags")
def show_tags_page():
    """shows tags page"""
    tags = Tag.query.all()
    return render_template("tags-page.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def show_tag_detail_page(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag-detail.html", tag=tag)

@app.route("/tags/new")
def show_new_tag_form():
    return render_template("new-tag.html")

@app.route("/tags/new", methods=["POST"])
def process_add_tag():
    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.")
    return redirect("/tags")

@app.route("/tags/<int:tag_id>/edit")
def show_edit_tag(tag_id):
    return render_template('edit-tag.html')

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete")
def delete_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")

#TODO GO BACK THROUGH ROUTES AND MAKE SURE THEY WORK
#TODO write tests











