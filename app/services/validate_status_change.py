def validate_status_change(trip, new_status):
    valid_transitions = {
        "PLANNED": ["ONGOING", "CANCELLED"],
        "ONGOING": ["COMPLETED", "CANCELLED"],
        "COMPLETED": [],
        "CANCELLED": []
    }

    if new_status not in valid_transitions.get(trip.status, []):
        return {
            "error": "INVALID_STATUS_TRANSITION",
            "message": f"Cannot change trip status from {trip.status} to {new_status}."
        }

    return None