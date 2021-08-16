from flask import Blueprint, request, render_template, url_for, flash
from flask_login import current_user
from werkzeug.utils import redirect

from winterhut import db
from winterhut.models.Post import Post
from winterhut.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/new_post", methods=["GET", "POST"])
def new_post_page():
    if not current_user.is_authenticated:
        flash("You must be logged in to see this page.")
        return redirect(url_for('users.login_page'))
    form = PostForm()
    if form.validate_on_submit():
        if form.save_as_draft.data:
            post = Post(title=form.title.data,
                        content=form.content.data,
                        is_draft=True,
                        user_id=current_user.id)
            flash("Post saved as draft successfully.")
        else:
            post = Post(title=form.title.data,
                        content=form.content.data,
                        is_draft=False,
                        user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("Post created successfully.")
        return redirect(url_for("posts.view_post_page", post_id=post.id))
    return render_template('new_post.html', form=form)


@posts.route("/post/<int:post_id>")
def view_post_page(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    return render_template('post.html', post=post)
