from flask_pot import db
import datetime

class Potholes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #posts = db.relationship('Post', backref='location', lazy=True)
    location = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Float())
    depth = db.Column(db.Float())
    photo = db.Column(db.String(20), default='default.jpg')
    serviced = db.Column(db.Integer, nullable=False)
    date_time_created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    date_created = db.Column(db.Date, nullable=False, default=datetime.datetime.now().date())
    date_completed = db.Column(db.DateTime, default=None)

    def __repr__(self):
        return f"Pothole('{self.location}', '{self.depth}', '{self.date_created}')"


class Drivers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Driver('{self.username}', '{self.id}', '{self.password}')"