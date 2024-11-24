from app import db

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), unique=True, nullable=False)
    title = db.Column(db.String(30), nullable=False)
    text = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'title': self.title,
            'text': self.text
        }