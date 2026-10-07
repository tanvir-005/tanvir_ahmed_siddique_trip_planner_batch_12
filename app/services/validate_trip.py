from datetime import date


def validate_trip(data):
    destination = data.get("destination")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    budget = data.get("budget")
    max_travelers = data.get("max_travelers")

    if not destination or not start_date or not end_date:
        return {
            "error": "INVALID_REQUEST",
            "message": "destination, start_date and end_date are required."
        }

    try:
        start_date = date.fromisoformat(start_date)
        end_date = date.fromisoformat(end_date)
    except (TypeError, ValueError):
        return {
            "error": "INVALID_DATE",
            "message": "Dates must use YYYY-MM-DD format."
        }

    if end_date <= start_date:
        return {
            "error": "INVALID_DATE_RANGE",
            "message": "end_date must be later than start_date."
        }

    if not isinstance(budget, (int, float)) or isinstance(budget, bool):
        return {
            "error": "INVALID_BUDGET",
            "message": "budget must be a number."
        }

    if budget <= 0:
        return {
            "error": "INVALID_BUDGET",
            "message": "budget must be greater than zero."
        }

    if not isinstance(max_travelers, int) or isinstance(max_travelers, bool):
        return {
            "error": "INVALID_CAPACITY",
            "message": "max_travelers must be an integer."
        }

    if max_travelers <= 0:
        return {
            "error": "INVALID_CAPACITY",
            "message": "max_travelers must be greater than zero."
        }

    return None