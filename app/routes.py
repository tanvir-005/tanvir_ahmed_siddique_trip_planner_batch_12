from flask import Blueprint, request
from datetime import date
from .models import db, Trip

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
    
    destination = data.get("destination")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    budget = data.get("budget")
    max_travelers = data.get("max_travelers")

    if not destination or not start_date or not end_date:
        return {
            "error": "INVALID_REQUEST", 
            "message": "destination, start_date and end_date are required"
        }, 400

    try:
        start_date = date.fromisoformat(start_date)
        end_date = date.fromisoformat(end_date)
    except ValueError:
        return {
            "error": "INVALID_DATE",
            "message": "Dates must use YYYY-MM-DD format."
        }, 400

    if end_date <= start_date:
        return {
            "error": "INVALID_DATE_RANGE",
            "message": "end_date must be later than start_date."
        }, 400
    
    if budget is None or budget <= 0:
        return {
            "error": "INVALID_BUDGET",
            "message": "budget must be greather zone"
        }, 400
    
    if max_travelers is None or max_travelers <= 0:
        return {
            "error": "INVALID_CAPACITY",
            "message": "max_travelers must be greater than zero."
        }, 400

    trip = Trip(
        destination = destination,
        start_date = start_date,
        end_date = end_date,
        budget = budget,
        max_travelers = max_travelers
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