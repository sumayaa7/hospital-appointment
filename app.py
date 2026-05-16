from __future__ import annotations


import os
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta

from dotenv import load_dotenv
from flask import Flask, abort, flash, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from rag_chat import RagAssistant

load_dotenv()

db = SQLAlchemy()
assistant: RagAssistant | None = None
chat_sessions: dict[str, list[dict[str, str]]] = {}


# Simple mapping name -> promo-style photo
DOCTOR_PHOTOS: dict[str, str] = {
    "Dr. Amina Rahman": "https://images.pexels.com/photos/5327585/pexels-photo-5327585.jpeg?auto=compress&cs=tinysrgb&w=400",
    "Dr. Daniel Kim": "https://images.pexels.com/photos/7578808/pexels-photo-7578808.jpeg?auto=compress&cs=tinysrgb&w=400",
    "Dr. Sofia Petrova": "https://images.pexels.com/photos/8460127/pexels-photo-8460127.jpeg?auto=compress&cs=tinysrgb&w=400",
}


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", secrets.token_hex(16)),
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "DATABASE_URL", f"sqlite:///{os.path.join(app.instance_path, 'app.db')}"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    os.makedirs(app.instance_path, exist_ok=True)
    db.init_app(app)

    register_routes(app)
    register_cli(app)

    global assistant
    try:
        assistant = RagAssistant()
    except Exception:
        assistant = None

    return app


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    specialty = db.Column(db.String(120), nullable=False)

    slots = db.relationship("Slot", back_populates="doctor", cascade="all, delete-orphan")

    @property
    def photo_url(self) -> str:
        return DOCTOR_PHOTOS.get(
            self.full_name,
            "https://images.pexels.com/photos/6129052/pexels-photo-6129052.jpeg?auto=compress&cs=tinysrgb&w=400",
        )


class Slot(db.Model):
    __tablename__ = "slots"
    __table_args__ = (
        UniqueConstraint("doctor_id", "start_at", name="uq_slot_doctor_start_at"),
    )

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)
    start_at = db.Column(db.DateTime, nullable=False, index=True)
    duration_min = db.Column(db.Integer, nullable=False, default=30)

    doctor = db.relationship("Doctor", back_populates="slots")
    appointment = db.relationship(
        "Appointment", back_populates="slot", uselist=False, cascade="all, delete-orphan"
    )

    @property
    def is_free(self) -> bool:
        return self.appointment is None or self.appointment.status != "BOOKED"


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)
    slot_id = db.Column(db.Integer, db.ForeignKey("slots.id"), nullable=False, unique=True)

    patient_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(40), nullable=False)

    status = db.Column(db.String(20), nullable=False, default="BOOKED")  # BOOKED | CANCELED
    cancel_token = db.Column(db.String(64), nullable=False, unique=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    slot = db.relationship("Slot", back_populates="appointment")


@dataclass(frozen=True)
class BookingForm:
    patient_name: str
    phone: str

    @staticmethod
    def from_request() -> "BookingForm":
        patient_name = (request.form.get("patient_name") or "").strip()
        phone = (request.form.get("phone") or "").strip()
        return BookingForm(patient_name=patient_name, phone=phone)

    def validate(self) -> list[str]:
        errors: list[str] = []
        if len(self.patient_name) < 2:
            errors.append("Patient name is required.")
        if len(self.phone) < 5:
            errors.append("Phone is required.")
        return errors


def register_routes(app: Flask) -> None:
    @app.post("/chat")
    def chat():
        global assistant
        data = request.get_json(silent=True) or {}
        message = (data.get("message") or "").strip()
        session_id = (data.get("session_id") or "default").strip()

        if not message:
            return jsonify({"answer": "Please enter a question.", "sources": []}), 400

        if assistant is None:
            return (
                jsonify(
                    {
                        "answer": "I'm not sure about that. Please contact support.",
                        "sources": [],
                    }
                ),
                503,
            )

        history = chat_sessions.get(session_id, [])
        try:
            result = assistant.answer(message, history)
        except Exception:
            return (
                jsonify(
                    {
                        "answer": "I'm not sure about that. Please contact support.",
                        "sources": [],
                    }
                ),
                503,
            )

        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": result["answer"]})
        chat_sessions[session_id] = history[-12:]

        return jsonify(result)

    @app.get("/")
    def index():
        now = datetime.now()
        horizon = now + timedelta(days=7)

        doctors = Doctor.query.order_by(Doctor.full_name.asc()).all()
        all_slots = (
            Slot.query.filter(Slot.start_at >= now, Slot.start_at <= horizon)
            .order_by(Slot.start_at.asc())
            .all()
        )

        # Build list of available dates (next 7 days that have at least one slot).
        available_dates: list[datetime.date] = sorted(
            {s.start_at.date() for s in all_slots}
        )
        if not available_dates:
            selected_date = None
        else:
            day_param = request.args.get("day")
            selected_date = available_dates[0]
            if day_param:
                try:
                    candidate = datetime.fromisoformat(day_param).date()
                    if candidate in available_dates:
                        selected_date = candidate
                except ValueError:
                    pass

        # For the selected date, group slots by doctor.
        slots_by_doctor: dict[int, list[Slot]] = {}
        if selected_date is not None:
            for s in all_slots:
                if s.start_at.date() == selected_date:
                    slots_by_doctor.setdefault(s.doctor_id, []).append(s)

        return render_template(
            "index.html",
            doctors=doctors,
            slots_by_doctor=slots_by_doctor,
            available_dates=available_dates,
            selected_date=selected_date,
        )

    @app.route("/slots/<int:slot_id>/book", methods=["GET", "POST"])
    def book(slot_id: int):
        slot = Slot.query.get_or_404(slot_id)
        if not slot.is_free:
            flash("This slot is already booked.", "error")
            return redirect(url_for("index"))

        if request.method == "GET":
            return render_template("book.html", slot=slot)

        form = BookingForm.from_request()
        errors = form.validate()
        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("book.html", slot=slot), 400

        # One-slot-one-appointment.
        # If there is an existing canceled appointment row for this slot,
        # reuse it instead of inserting a second row (to satisfy DB uniqueness).
        existing = slot.appointment
        if existing is not None:
            if existing.status == "BOOKED":
                flash("This slot is already booked.", "error")
                return redirect(url_for("index"))
            appt = existing
            appt.patient_name = form.patient_name
            appt.phone = form.phone
            appt.status = "BOOKED"
            appt.cancel_token = secrets.token_urlsafe(24)
            appt.created_at = datetime.utcnow()
        else:
            appt = Appointment(
                slot=slot,
                patient_name=form.patient_name,
                phone=form.phone,
                status="BOOKED",
                cancel_token=secrets.token_urlsafe(24),
            )
            db.session.add(appt)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash("Could not book this slot (it may have been taken). Try another one.", "error")
            return redirect(url_for("index"))

        return render_template("success.html", appointment=appt)

    @app.get("/cancel/<string:token>")
    def cancel(token: str):
        appt = Appointment.query.filter_by(cancel_token=token).first()
        if not appt:
            abort(404)
        # For this demo we treat cancellation as deletion,
        # so the same time slot can be booked again cleanly.
        db.session.delete(appt)
        db.session.commit()
        flash("Appointment canceled. The slot is now free again.", "success")
        return redirect(url_for("index"))

    @app.get("/admin/appointments")
    def admin_appointments():
        appts = (
            Appointment.query.join(Appointment.slot)
            .join(Slot.doctor)
            .order_by(Slot.start_at.desc())
            .all()
        )
        return render_template("admin.html", appointments=appts)


def register_cli(app: Flask) -> None:
    @app.cli.command("init-db")
    def init_db_command():
        init_db(app)
        print("Initialized database with demo data.")


def init_db(app: Flask) -> None:
    with app.app_context():
        db.drop_all()
        db.create_all()

        doctors = [
            Doctor(full_name="Dr. Amina Rahman", specialty="Cardiology"),
            Doctor(full_name="Dr. Daniel Kim", specialty="Dermatology"),
            Doctor(full_name="Dr. Sofia Petrova", specialty="Pediatrics"),
        ]
        db.session.add_all(doctors)
        db.session.flush()

        now = datetime.now().replace(minute=0, second=0, microsecond=0)
        # First day = today (slots in the past are filtered out on the index page)
        start_day = now.replace(hour=9)

        slots: list[Slot] = []
        for d in doctors:
            for day in range(0, 5):  # next 5 days
                day_start = start_day + timedelta(days=day)
                # compact 6-hour window: 09:00–14:00
                for h in (9, 10, 11, 12, 13, 14):
                    slots.append(
                        Slot(
                            doctor_id=d.id,
                            start_at=day_start.replace(hour=h),
                            duration_min=30,
                        )
                    )

        db.session.add_all(slots)
        db.session.commit()


def main() -> None:
    app = create_app()

    # Small convenience "python app.py ..." wrapper for beginners
    import sys

    if len(sys.argv) >= 2 and sys.argv[1] in {"init-db", "run"}:
        cmd = sys.argv[1]
        if cmd == "init-db":
            init_db(app)
            print("Initialized database with demo data.")
            return
        if cmd == "run":
            app.run(debug=True)
            return

    print("Usage:")
    print("  py app.py init-db")
    print("  py app.py run")


if __name__ == "__main__":
    main()

