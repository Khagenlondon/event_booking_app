
from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from models import db, Event, Booking

booking_bp = Blueprint("booking", __name__)

@booking_bp.route("/book/<int:event_id>", methods=["POST"])
@login_required
def book_event(event_id):
    event = Event.query.get_or_404(event_id)
    try:
        quantity = int(request.form.get("quantity", "1"))
    except ValueError:
        flash("Invalid quantity.", "error")
        return redirect(url_for("events.event_detail", event_id=event_id))

    if quantity <= 0:
        flash("Quantity must be positive.", "error")
        return redirect(url_for("events.event_detail", event_id=event_id))

    # Preventing overbooking
    if quantity > event.remaining_capacity:
        flash("Not enough remaining capacity.", "error")
        return redirect(url_for("events.event_detail", event_id=event_id))

    booking = Booking(user_id=current_user.id, event_id=event.id, quantity=quantity)
    db.session.add(booking)
    db.session.commit()
    flash("Booking successful!", "success")
    return redirect(url_for("booking.my_bookings"))

@booking_bp.route("/bookings")
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template("bookings.html", bookings=bookings)


@booking_bp.route("/cancel/<int:booking_id>", methods=["POST"])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    # Ensuring users can only cancel their own bookings
    if booking.user_id != current_user.id:
        flash("You are not allowed to cancel this booking.", "error")
        return redirect(url_for("booking.my_bookings"))

    db.session.delete(booking)
    db.session.commit()

    flash("Booking cancelled successfully.", "success")
    return redirect(url_for("booking.my_bookings"))