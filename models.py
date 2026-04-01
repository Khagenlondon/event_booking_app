
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# User model (OOP and ORM)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(80), nullable=False)

    bookings = db.relationship("Booking", backref="user", lazy=True)

# Event model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    datetime = db.Column(db.String(50), nullable=False)  # keep simple (string)
    capacity = db.Column(db.Integer, nullable=False)

    bookings = db.relationship("Booking", backref="event", lazy=True)

    @property
    def remaining_capacity(self):
        # Calculate remaining capacity from bookings
        booked = sum(b.quantity for b in self.bookings)
        return self.capacity - booked

# Booking model
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
