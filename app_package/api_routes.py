
from flask import Blueprint, jsonify
from models import Event

api_bp = Blueprint("api", __name__)

@api_bp.get("/events")
def api_events():
    # JSON API for events
    events = Event.query.all()
    data = [
        {
            "id": e.id,
            "name": e.name,
            "location": e.location,
            "datetime": e.datetime,
            "capacity": e.capacity,
            "remaining_capacity": e.remaining_capacity,
        }
        for e in events
    ]
    return jsonify(data)

@api_bp.get("/events/<int:event_id>/remaining")
def api_event_remaining(event_id):
    # synchronously fetch remaining capacity
    event = Event.query.get_or_404(event_id)
    return jsonify({"remaining_capacity": event.remaining_capacity})
