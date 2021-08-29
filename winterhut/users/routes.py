import datetime
import logging
from flask import Blueprint, request, render_template, url_for, flash
from flask_login import current_user, login_user
from werkzeug.utils import redirect

from winterhut import bcrypt, db
from winterhut.models.IpBan import IpBan
from winterhut.models.User import User
from winterhut.users.forms import LoginForm

users = Blueprint('users', __name__)
log = logging.getLogger()


@users.route("/login", methods=["GET", "POST"])
def login_page():
    log.info("Login Page requested")
    if current_user.is_authenticated:
        log.info(f"Current user '{current_user.username}' is already authenticated, returning to landing page")
        return redirect(url_for('main.home_page'))
    ip_address = request.access_route[0]
    ip_of_visitor = IpBan.query.filter_by(ip=ip_address).first()
    if ip_of_visitor:
        if ip_of_visitor.login_attempts >= 5:
            log.warning(f"IP Address '{ip_address}' is banned")
            flash("Uh oh, seems like you are banned from performing this action :(")
            return render_template('banned.html', title="Ban(an)ned | Winter's Hut"), 403
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            log.info(f"User '{user.username}' authenticated successfully, sending e-mail token")
            flash("Password authentication successful, sending token to associated e-mail.")
            user.send_token_email()
            return redirect(url_for('main.home_page'))
        else:
            log.info(f"IP Address '{ip_address}' failed password authentication")
            flash("Nuh-uh, that wasn't it, try again.")
            if ip_of_visitor:
                ip_of_visitor.login_attempts += 1
                ip_of_visitor.last_attempt = datetime.datetime.utcnow()
                db.session.add(ip_of_visitor)
                db.session.commit()
            else:
                record_ip = IpBan(ip=ip_address, login_attempts=1)
                db.session.add(record_ip)
                db.session.commit()
    return render_template('login.html', title="Login | Winter's Hut", form=form)


@users.route("/logmein/<token>", methods=["GET", "POST"])
def log_me_in_page(token):
    log.info(f"Token authentication received for token - {token}")
    if current_user.is_authenticated:
        log.info(f"Current user '{current_user.username}' is already authenticated, returning to landing page")
        return redirect(url_for('main.home_page'))
    ip_address = request.access_route[0]
    ip_of_visitor = IpBan.query.filter_by(ip=ip_address).first()
    if ip_of_visitor:
        if ip_of_visitor.login_attempts >= 5:
            log.warning(f"IP Address '{ip_address}' is banned")
            flash("Uh oh, seems like you are banned from performing this action :(")
            return render_template('banned.html', title="Ban(an)ned | Winter's Hut"), 403
    user = User.verify_token(token)
    if user is None:
        log.info(f"IP Address '{ip_address}' failed token authentication")
        flash("Nuh-uh, that wasn't it")
        if ip_of_visitor:
            ip_of_visitor.login_attempts += 1
            ip_of_visitor.last_attempt = datetime.datetime.utcnow()
            db.session.add(ip_of_visitor)
            db.session.commit()
        else:
            record_ip = IpBan(ip=ip_address, login_attempts=1)
            db.session.add(record_ip)
            db.session.commit()
        return redirect(url_for('users.login_page'))
    login_user(user)
    log.info(f"User '{user.username}' verified login token")
    flash(f"Token verified, welcome on board, {user.username}")
    return redirect(url_for('main.home_page'))
