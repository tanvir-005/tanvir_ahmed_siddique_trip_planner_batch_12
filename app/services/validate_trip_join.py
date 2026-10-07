def validate_trip_join(trip, traveler):
    if trip.status != "PLANNED":
        return {
            "error": "TRIP_NOT_OPEN",
            "message": "Travelers can only be added to planned trips."
        }

    if len(trip.travelers) >= trip.max_travelers:
        return {
            "error": "TRIP_FULL",
            "message": "The trip has reached its maximum traveler capacity."
        }

    if traveler in trip.travelers:
        return {
            "error": "DUPLICATE_TRAVELER",
            "message": "This traveler is already in the trip."
        }

    for other_trip in traveler.trips:
        if (other_trip.start_date < trip.end_date and other_trip.end_date > trip.start_date):
            return {
                "error": "TRIP_OVERLAP",
                "message": "The traveler is already participating in an overlapping trip."
            }

    return None