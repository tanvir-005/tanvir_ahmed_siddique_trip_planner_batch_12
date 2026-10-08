from datetime import date
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

    new_start_date = date.fromisoformat(data["start_date"])
    new_end_date = date.fromisoformat(data["end_date"])
    new_budget = data["budget"]
    new_max_travelers = data["max_travelers"]

    # max traveler and traveler count check
    if new_max_travelers < len(trip.travelers):
        return {
            "error": "MAX_TRAVELERS_TOO_LOW",
            "message": "max_travelers must not be reduced below the current traveler count."
        }

    # expense and budget check
    current_total_expenses = sum(expense.amount for expense in trip.expenses)
    if new_budget < current_total_expenses:
        return {
            "error": "BUDGET_EXCEEDED",
            "message": "Trip budget cannot be lower than the current total expenses."
        }

    # travelers' trip conflict check
    for traveler in trip.travelers:
        for other_trip in traveler.trips:
            if other_trip.id == trip.id:
                continue
            if other_trip.start_date < new_end_date and other_trip.end_date > new_start_date:
                return {
                    "error": "TRIP_OVERLAP",
                    "message": "Updating trip dates would cause an overlapping trip for a traveler."
                }

    return None