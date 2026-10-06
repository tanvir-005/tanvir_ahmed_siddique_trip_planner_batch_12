from flask import Blueprint, request
from datetime import date
from .models import db, Trip
from .services import validate_trip

# Blueprint initialization
blueprint = Blueprint("main", __name__)

# /health route to get json and 200 status code
@blueprint.get("/health")
def health():
    return {"status": "ok"}, 200

# /api/v1/trips route (POST) to create a trip
@blueprint.post("/api/v1/trips")
def create_trip():
    data = request.get_json()

    if not data:
        return {
            "error": "INVALID_REQUEST",
            "message": "Request body is required."
        }, 400

    error = validate_trip_data(data)

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

    return {
        "id": trip.id,
        "destination": trip.destination,
        "start_date": trip.start_date.isoformat(),
        "end_date": trip.end_date.isoformat(),
        "budget": trip.budget,
        "max_travelers": trip.max_travelers,
        "status": trip.status
    }, 201

# /api/v1/trips route (GET) to show a trip
@blueprint.get("/api/v1/trips/<int:trip_id>")
def get_trip(trip_id):
    trip = Trip.query.get(trip_id)

    if trip is None:
        return {
            "error": "TRIP_NOT_FOUND",
            "message": "Trip not found."
        }, 404

    return {
        "id": trip.id,
        "destination": trip.destination,
        "start_date": trip.start_date.isoformat(),
        "end_date": trip.end_date.isoformat(),
        "budget": trip.budget,
        "max_travelers": trip.max_travelers,
        "status": trip.status
    }, 200

# route (GET) to show all trips
@blueprint.get("/api/v1/trips")
def get_trips():
    trips = Trip.query.all()

    return [
        {
            "id": trip.id,
            "destination": trip.destination,
            "start_date": trip.start_date.isoformat(),
            "end_date": trip.end_date.isoformat(),
            "budget": trip.budget,
            "max_travelers": trip.max_travelers,
            "status": trip.status
        }
        for trip in trips
    ], 200

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

    error = validate_trip_data(data)

    if error:
        return error, 400

    trip.destination = data["destination"]
    trip.start_date = date.fromisoformat(data["start_date"])
    trip.end_date = date.fromisoformat(data["end_date"])
    trip.budget = data["budget"]
    trip.max_travelers = data["max_travelers"]

    db.session.commit()

    return {
        "id": trip.id,
        "destination": trip.destination,
        "start_date": trip.start_date.isoformat(),
        "end_date": trip.end_date.isoformat(),
        "budget": trip.budget,
        "max_travelers": trip.max_travelers,
        "status": trip.status
    }, 200

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

