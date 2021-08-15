from datetime import datetime
from winterhut import db


class IpBan(db.Model):
    __tablename__ = 'ip_bans'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50), unique=True, nullable=False)
    login_attempts = db.Column(db.Integer, nullable=False, default=0)
    first_attempt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_attempt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"IpBan('{self.ip}', '{self.first_attempt}', '{self.last_attempt}')"
