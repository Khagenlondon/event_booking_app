
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # form handling with validation
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        name = request.form.get("name", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not name or not password:
            flash("All fields are required.", "error")
            return render_template("register.html")

        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("Email already registered.", "error")
            return render_template("register.html")

        hashed = generate_password_hash(password)
        user = User(email=email, name=name, password=hashed)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Invalid credentials.", "error")
            return render_template("login.html")

        login_user(user)
        flash("Logged in successfully.", "success")
        return redirect(url_for("events.list_events"))

    return render_template("login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "success")
    return redirect(url_for("auth.login"))

@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Name cannot be empty.", "error")
        else:
            current_user.name = name
            db.session.commit()
            flash("Profile updated.", "success")
    return render_template("profile.html")
