from flask import Blueprint, request, render_template

from winterhut.models.Post import Post

main = Blueprint('main', __name__)


@main.route("/")
def home_page():
    page = request.args.get('page', default=1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=1)
    return render_template('home.html', title="Winter's Hut", blog_posts=posts)


@main.route("/cv")
def cv_page():
    return render_template('cv.html')
