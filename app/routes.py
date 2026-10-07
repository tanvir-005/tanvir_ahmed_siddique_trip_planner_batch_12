from flask import Blueprint, request
from datetime import date
from .models import db, Trip, Traveler
from .services import validate_trip, validate_change, trip_dictonarize, validate_traveler, validate_trip_join


# Blueprint initialization
blueprint = Blueprint("main", __name__)


# -------------- GET : /
# / route to get a message that the project is running
@blueprint.get("/")
def home():
    return {"success": "project is running"}, 200


# -------------- GET : /health
# /health route to get json and 200 status code
@blueprint.get("/health")
def health():
    return {"status": "ok"}, 200


# -------------- POST : /api/v1/trips
# /api/v1/trips route (POST) to create a trip
@blueprint.post("/api/v1/trips")
def create_trip():
    data = request.get_json()

    if not data:
        return {
            "error": "INVALID_REQUEST",
            "message": "Request body is required."
        }, 400

    error = validate_trip(data)

    if error:
        return error, 400

    trip = Trip(
        destination=data["destination"],
        start_date=date.fromisoformat(data["start_date"]),
        end_date=date.fromisoformat(data["end_date"]),
        budget=data["budget"],
        max_travelers=data["max_travelers"]
    )

    db.session.add(trip)
    db.session.commit()

    return trip_dictonarize(trip), 201


# -------------- GET : /api/v1/trips/<int:trip_id>
# /api/v1/trips route (GET) to show a trip
@blueprint.get("/api/v1/trips/<int:trip_id>")
def get_trip(trip_id):
    trip = Trip.query.get(trip_id)

    if trip is None:
        return {
            "error": "TRIP_NOT_FOUND",
            "message": "Trip not found."
        }, 404

    return trip_dictonarize(trip), 200


# -------------- GET : /api/v1/trips
# route (GET) to show all trips
@blueprint.get("/api/v1/trips")
def get_trips():
    trips = Trip.query.all()

    return [
        trip_dictonarize(trip)
        for trip in trips
    ], 200


# -------------- PUT : /api/v1/trips/<int:trip_id>
# route (PUT) to update a trip
@blueprint.put("/api/v1/trips/<int:trip_id>")
def update_trip(trip_id):
    trip = Trip.query.get(trip_id)

    if trip is None:
        return {
            "error": "TRIP_NOT_FOUND",
            "message": "Trip not found."
        }, 404

    data = request.get_json()

    if not data:
        return {
            "error": "INVALID_REQUEST",
            "message": "Request body is required."
        }, 400

    error = validate_change(trip, data)

    if error:
        return error, 409 if error["error"] == "TRIP_NOT_EDITABLE" else 400

    trip.destination = data["destination"]
    trip.start_date = date.fromisoformat(data["start_date"])
    trip.end_date = date.fromisoformat(data["end_date"])
    trip.budget = data["budget"]
    trip.max_travelers = data["max_travelers"]

    db.session.commit()

    return trip_dictonarize(trip), 200


# -------------- DELETE : /api/v1/trips/<int:trip_id>
# route (DELETE) to delete a trip
@blueprint.delete("/api/v1/trips/<int:trip_id>")
def delete_trip(trip_id):
    trip = Trip.query.get(trip_id)

    if trip is None:
        return {
            "error": "TRIP_NOT_FOUND",
            "message": "Trip not found."
        }, 404

    db.session.delete(trip)
    db.session.commit()

    return {
        "message": "Trip deleted successfully."
    }, 200


# -------------- POST : /api/v1/trips/<int:trip_id>/travelers
# route to add a traveler to a trip
@blueprint.post("/api/v1/trips/<int:trip_id>/travelers")
def add_traveler(trip_id):
    trip = Trip.query.get(trip_id)

    if trip is None:
        return {
            "error": "TRIP_NOT_FOUND",
            "message": "Trip not found."
        }, 404

    data = request.get_json()

    if not data:
        return {
            "error": "INVALID_REQUEST",
            "message": "Request body is required."
        }, 400

    error = validate_traveler(data)

    if error:
        return error, 400

    traveler = Traveler.query.filter_by(
        email=data["email"]
    ).first()

    if traveler is None:
        traveler = Traveler(
            name=data["name"],
            email=data["email"]
        )

    error = validate_trip_join(trip, traveler)

    if error:
        return error, 409

    db.session.add(traveler)
    trip.travelers.append(traveler)
    db.session.commit()

    return {
        "id": traveler.id,
        "name": traveler.name,
        "email": traveler.email
    }, 201