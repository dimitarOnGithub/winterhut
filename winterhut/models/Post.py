from datetime import datetime
from winterhut import db


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    is_draft = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

    def dump_as_json(self):
        return {
            "id": f"{self.id}",
            "title": f"{self.title}",
            "date_posted": f"{self.date_posted.isoformat()}",
            "content": f"{self.content}",
            "is_draft": f"{self.is_draft}",
            "user_id": f"{self.user_id}"
        }

    def load_from_json(self, json):
        print(json)
        self.id = json.get('id')
        self.title = json.get('title')
        self.date_posted = datetime.fromisoformat(json.get('date_posted'))
        self.content = json.get('content')
        self.is_draft = json.get('is_draft')
        self.user_id = json.get('user_id')
