from .validate_trip import validate_trip


def validate_change(trip, data):
    # Completed and cancelled trips cannot be edited.
    if trip.status in ["COMPLETED", "CANCELLED"]:
        return {
            "error": "TRIP_NOT_EDITABLE",
            "message": "Completed or cancelled trips cannot be edited."
        }

    # Validate the new trip data.
    error = validate_trip(data)

    if error:
        return error

    return None