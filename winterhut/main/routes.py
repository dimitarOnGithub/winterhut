from flask import Blueprint, request, render_template

from winterhut.models.Post import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/page/<int:page>")
def home_page(page=1):
    page_from_url = page
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page_from_url, per_page=1)
    return render_template('home.html', title="Winter's Hut", blog_posts=posts, page_from_url=page_from_url)


@main.route("/cv")
def cv_page():
    return render_template('cv.html')
