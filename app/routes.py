from flask import Blueprint, request
from datetime import date
from .models import db, Trip, Traveler, Expense
from .services import validate_trip, validate_change, trip_dictonarize, validate_traveler, validate_trip_join, validate_expense, validate_status_change, trip_summary


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
        status_code = 409 if error["error"] in [
            "TRIP_NOT_EDITABLE",
            "MAX_TRAVELERS_TOO_LOW",
            "BUDGET_EXCEEDED",
            "TRIP_OVERLAP"
        ] else 400
        return error, status_code

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


# -------------- POST : /api/v1/trips/<int:trip_id>/expenses
# route to add an expense to a trip
@blueprint.post("/api/v1/trips/<int:trip_id>/expenses")
def add_expense(trip_id):
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

    error = validate_expense(data)

    if error:
        return error, 400

    if trip.status in ["COMPLETED", "CANCELLED"]:
        return {
            "error": "TRIP_NOT_EDITABLE",
            "message": "Completed or cancelled trips cannot have expenses."
        }, 409

    total_expenses = sum(
        expense.amount
        for expense in trip.expenses
    )

    if total_expenses + data["amount"] > trip.budget:
        return {
            "error": "BUDGET_EXCEEDED",
            "message": "Total expenses cannot exceed the trip budget."
        }, 409

    expense = Expense(
        title=data["title"],
        amount=data["amount"],
        trip=trip
    )

    db.session.add(expense)
    db.session.commit()

    return {
        "id": expense.id,
        "title": expense.title,
        "amount": expense.amount
    }, 201


# -------------- DELETE : /api/v1/trips/<int:trip_id>/travelers/<int:traveler_id>
# route to remove a traveler from a trip
@blueprint.delete("/api/v1/trips/<int:trip_id>/travelers/<int:traveler_id>")
def remove_traveler(trip_id, traveler_id):
    trip = Trip.query.get(trip_id)

    if trip is None:
        return {
            "error": "TRIP_NOT_FOUND",
            "message": "Trip not found."
        }, 404

    traveler = Traveler.query.get(traveler_id)

    if traveler is None:
        return {
            "error": "TRAVELER_NOT_FOUND",
            "message": "Traveler not found."
        }, 404

    if traveler not in trip.travelers:
        return {
            "error": "TRAVELER_NOT_IN_TRIP",
            "message": "Traveler is not part of this trip."
        }, 404

    if trip.status in ["COMPLETED", "CANCELLED"]:
        return {
            "error": "TRIP_NOT_EDITABLE",
            "message": "Completed or cancelled trips cannot be modified."
        }, 409

    trip.travelers.remove(traveler)
    db.session.commit()

    return {
        "message": "Traveler removed successfully."
    }, 200


# -------------- PATCH : /api/v1/trips/<int:trip_id>/status
# route to change the status of a trip
@blueprint.patch("/api/v1/trips/<int:trip_id>/status")
def change_status(trip_id):
    trip = Trip.query.get(trip_id)

    if trip is None:
        return {
            "error": "TRIP_NOT_FOUND",
            "message": "Trip not found."
        }, 404

    data = request.get_json()

    if not data or "status" not in data:
        return {
            "error": "INVALID_REQUEST",
            "message": "status is required."
        }, 400

    new_status = data["status"]

    if new_status not in ["PLANNED", "ONGOING", "COMPLETED", "CANCELLED"]:
        return {
            "error": "INVALID_STATUS",
            "message": "Invalid trip status."
        }, 400

    error = validate_status_change(trip, new_status)

    if error:
        return error, 409

    trip.status = new_status
    db.session.commit()

    return trip_dictonarize(trip), 200


# -------------- GET : /api/v1/trips/<int:trip_id>/summary
# route to show trip summary
@blueprint.get("/api/v1/trips/<int:trip_id>/summary")
def get_trip_summary(trip_id):
    trip = Trip.query.get(trip_id)

    if trip is None:
        return {
            "error": "TRIP_NOT_FOUND",
            "message": "Trip not found."
        }, 404

    return trip_summary(trip), 200