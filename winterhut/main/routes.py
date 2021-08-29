from flask import Blueprint, request, render_template, flash, url_for
from flask_login import current_user
from werkzeug.utils import redirect
import logging
from winterhut import db
from winterhut.models.IpBan import IpBan
from winterhut.models.Post import Post
from winterhut.main.forms import IpBanForm

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
