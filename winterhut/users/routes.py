from flask import Blueprint, request, render_template, url_for
from flask_login import current_user
from werkzeug.utils import redirect

from winterhut.user.forms import LoginForm

user = Blueprint('user', __name__)


@user.route("/login", methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('main.home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful :( Please try again', 'danger')
    return render_template('login.html', title="Login | Winter's Hut", form=form)
