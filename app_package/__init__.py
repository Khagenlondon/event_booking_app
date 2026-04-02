
from flask import Flask
from flask_login import LoginManager
from models import db, User
from config import Config
import os

login_manager = LoginManager()
login_manager.login_view = "auth.login" 

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    # Ensuring instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Init extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Registering blueprints
    from .auth_routes import auth_bp
    from .event_routes import event_bp
    from .booking_routes import booking_bp
    from .api_routes import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(event_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    # Creating tables and seed events
    with app.app_context():
        db.create_all()
        seed_events()

    return app

def seed_events():
    from models import Event
    if Event.query.count() == 0:
        sample_events = [
            Event(
                name="London Tech Show",
                description="A simple tech conference.",
                location="London",
                datetime="2026-05-02 10:00",
                capacity=100,
            ),
            Event(
                name="Music Festival",
                description="Outdoor music festival.",
                location="Manchester",
                datetime="2026-06-15 12:00",
                capacity=200,
            ),
        ]
        db.session.add_all(sample_events)
        db.session.commit()
