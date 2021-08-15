from flask import current_app, url_for
from flask_login import UserMixin
from winterhut import db, login_manager, mail
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    user_posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def get_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('UTF-8')

    @staticmethod
    def verify_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except (SignatureExpired, BadSignature):
            return None
        return User.query.get(user_id)

    def send_token_email(self):
        token = self.get_token()
        msg = Message("Winter's Hut Login Token", sender='noreply@sudosuwinter.me',
                      recipients=[self.email])
        msg.body = f"""
    Beep-boop, here's your login token, boss:
    {url_for('users.log_me_in_page', token=token, _external=True)}
    If you did not make this request, someone knows your password, lol.
    """
        print(msg)
        mail.send(msg)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
