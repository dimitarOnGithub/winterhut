import json
from datetime import datetime
import ast
from flask import Blueprint, request, render_template, flash, url_for
from flask_login import current_user
from werkzeug.utils import redirect
import os
import logging
from winterhut import db
from winterhut.models.IpBan import IpBan
from winterhut.models.Post import Post
from winterhut.main.forms import IpBanForm, ImporterForm
from winterhut.utils.importer import Importer

main = Blueprint('main', __name__)
log = logging.getLogger()


@main.route("/")
@main.route("/page/<int:page>")
def home_page(page=1):
    log.info(f"Landing page requested")
    page_from_url = page
    posts = Post.query.filter_by(is_draft=0).order_by(Post.date_posted.desc())\
        .paginate(page=page_from_url, per_page=1)
    return render_template('home.html', title="Winter's Hut", blog_posts=posts, page_from_url=page_from_url)


@main.route("/level80paladin")
def cv_page():
    log.info(f"CV page requested")
    return render_template('cv.html')


@main.route("/ban_ip", methods=["GET", "POST"])
def ban_ip_page():
    log.info(f"Ban IP page requested")
    if not current_user.is_authenticated:
        log.warning(f"User requesting page is not authenticated, returning to login page")
        flash("You must be logged in to see this page.")
        return redirect(url_for('users.login_page'))
    form = IpBanForm()
    if form.validate_on_submit():
        ip_ban = IpBan(ip=form.ip_address.data, login_attempts=5)
        db.session.add(ip_ban)
        db.session.commit()
        log.info(f"Ban IP form validated, {ip_ban.ip} banned")
        flash(f"IP address '{ip_ban.ip}' banned successfully.")
    return render_template('ban_ip.html', form=form)


@main.route("/importer", methods=["GET", "POST"])
def importer_page():
    log.info(f"Importer page requested")
    if not current_user.is_authenticated:
        log.warning(f"User requesting page is not authenticated, returning to login page")
        flash("You must be logged in to see this page.")
        return redirect(url_for('users.login_page'))
    form = ImporterForm()
    if form.validate_on_submit():
        uploaded_file = request.files['file']
        uploaded_file.save(os.path.join('winterhut/static/', uploaded_file.filename))
        return redirect(url_for('main.importer_data_page', file=f"{uploaded_file.filename}"))
    return render_template('importer_main.html', form=form)


@main.route("/importer_data", methods=["GET", "POST"])
def importer_data_page():
    file = request.args['file']
    file_path = os.path.join("winterhut", "static", file)
    file = open(file_path)
    importer = Importer(file)
    json_data = importer.load_file_content()
    articles = json_data.get('articles')
    prepared_articles = []
    for article_id, article_data in articles.items():
        article_post = Post()
        article_post.title = article_data.get('title')
        article_post.content = article_data.get('content')
        article_post.date_posted = datetime.fromisoformat(article_data.get('published_date'))
        article_post.is_draft = 1
        article_post.user_id = 1
        setattr(article_post, "json_id", article_id)
        prepared_articles.append(article_post)
    return render_template('importer_data.html', data=prepared_articles, file_path=file_path)


@main.route("/preview")
def preview_post_page():
    post_id = request.args['post_id']
    file_path = request.args['file_path']
    file = open(file_path)
    importer = Importer(file)
    json_data = importer.load_file_content()
    articles = json_data.get('articles')
    for article_id, article_data in articles.items():
        if article_id == post_id:
            article_post = Post()
            article_post.title = article_data.get('title')
            article_post.content = article_data.get('content')
            article_post.date_posted = datetime.fromisoformat(article_data.get('published_date'))
            article_post.is_draft = 1
            article_post.user_id = 1
    return render_template('post.html', post=article_post, preview=1)


@main.route("/import")
def import_data():
    file_path = request.args['file_path']
    file = open(file_path)
    importer = Importer(file)
    json_data = importer.load_file_content()
    articles = json_data.get('articles')
    for article_id, article_data in articles.items():
        article_post = Post()
        article_post.title = article_data.get('title')
        article_post.content = article_data.get('content')
        article_post.date_posted = datetime.fromisoformat(article_data.get('published_date'))
        article_post.is_draft = 1
        article_post.user_id = 1
        db.session.add(article_post)
        db.session.commit()
    return redirect(url_for('posts.posts_list_page'))
