from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

trip_traveler = db.Table(
    "trip_traveler",
    db.Column("trip_id", db.Integer, db.ForeignKey("trip.id"), primary_key=True),
    db.Column("traveler_id", db.Integer, db.ForeignKey("traveler.id"), primary_key=True)
)

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    max_travelers = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="PLANNED")

    travelers = db.relationship(
        "Traveler",
        secondary=trip_traveler,
        back_populates="trips"
    )

    expenses = db.relationship(
        "Expense",
        backref="trip",
        cascade="all, delete-orphan"
    )

class Traveler(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)

    trips = db.relationship(
        "Trip",
        secondary=trip_traveler,
        back_populates="travelers"
    )

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    trip_id = db.Column(
        db.Integer,
        db.ForeignKey("trip.id"),
        nullable=False
    )