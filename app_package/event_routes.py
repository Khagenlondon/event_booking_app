
from flask import Blueprint, render_template
from flask_login import login_required
from models import Event

event_bp = Blueprint("events", __name__)

@event_bp.route("/")
def home():
    return list_events()

@event_bp.route("/events")
def list_events():
    events = Event.query.all()
    return render_template("events.html", events=events)

@event_bp.route("/events/<int:event_id>")
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template("event_detail.html", event=event)
