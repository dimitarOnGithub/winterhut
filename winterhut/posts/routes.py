import logging
from flask import Blueprint, request, render_template, url_for, flash
from flask_login import current_user
from werkzeug.utils import redirect

from winterhut import db
from winterhut.models.Post import Post
from winterhut.posts.forms import PostForm

posts = Blueprint('posts', __name__)
log = logging.getLogger()


@posts.route("/new_post", methods=["GET", "POST"])
def new_post_page():
    log.info(f"New Post page requested")
    if not current_user.is_authenticated:
        log.warning(f"User requesting page is not authenticated, returning to login page")
        flash("You must be logged in to see this page.")
        return redirect(url_for('users.login_page'))
    form = PostForm()
    if form.validate_on_submit():
        if form.save_as_draft.data:
            post = Post(title=form.title.data,
                        content=form.content.data,
                        is_draft=True,
                        user_id=current_user.id)
            log.info(f"Post with id '{post.id}' saved as draft successfully")
            flash("Post saved as draft successfully.")
        else:
            post = Post(title=form.title.data,
                        content=form.content.data,
                        is_draft=False,
                        user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        log.info(f"Post with id '{post.id}' posted successfully")
        flash("Post created successfully.")
        return redirect(url_for("posts.view_post_page", post_id=post.id))
    return render_template('new_post.html', form=form)


@posts.route("/post/<int:post_id>")
def view_post_page(post_id):
    log.info(f"View Post page requested")
    if current_user.is_authenticated:
        post = Post.query.filter_by(id=post_id).first_or_404()
        if post.is_draft == 1:
            flash("You are viewing a draft post.")
    else:
        post = Post.query.filter_by(id=post_id, is_draft=0).first_or_404()
    return render_template('post.html', post=post)


@posts.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
def edit_post_page(post_id):
    log.info(f"Edit Post page requested")
    if not current_user.is_authenticated:
        log.warning(f"User requesting page is not authenticated, returning to login page")
        flash("You must be logged in to see this page.")
        return redirect(url_for('users.login_page'))
    post = Post.query.filter_by(id=post_id).first_or_404()
    form = PostForm()
    if form.validate_on_submit():
        if form.save_as_draft.data:
            post.title = form.title.data
            post.content = form.content.data
            post.is_draft = True
            db.session.commit()
            log.info(f"Post with id '{post.id}' saved as draft successfully")
            flash("Post saved as draft successfully.")
        else:
            post.title = form.title.data
            post.content = form.content.data
            post.is_draft = False
            db.session.commit()
            log.info(f"Post with id '{post.id}' edited successfully")
            flash("Post edited successfully.")
        return redirect(url_for("posts.view_post_page", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("edit_post.html", title="Edit Post", form=form)


@posts.route("/posts_list")
def posts_list_page():
    log.info(f"Posts list page requested")
    if not current_user.is_authenticated:
        log.warning(f"User requesting page is not authenticated, returning to login page")
        flash("You must be logged in to see this page.")
        return redirect(url_for('users.login_page'))
    view_filter = request.args.get('view', default="all", type=str)
    if view_filter == "all":
        log.info(f"List of all posts requested")
        all_posts = Post.query.order_by(Post.date_posted.desc())
    elif view_filter == "drafts":
        log.info(f"List of only draft posts requested")
        all_posts = Post.query.filter_by(is_draft=1).order_by(Post.date_posted.desc())
    elif view_filter == "live":
        log.info(f"List of only live posts requested")
        all_posts = Post.query.filter_by(is_draft=0).order_by(Post.date_posted.desc())
    else:
        log.warning(f"Unknown URL parameter: {view_filter}, returning all posts")
        flash(f"Unknown URL parameter: {view_filter}")
        return redirect(url_for("posts.posts_list_page"))
    return render_template('posts_list.html', posts=all_posts)


@posts.route("/all_posts")
def all_posts_page():
    log.info(f"All Posts page requested")
    all_posts = Post.query.filter_by(is_draft=0).order_by(Post.date_posted.desc())
    return render_template('all_blog_posts.html', posts=all_posts)
