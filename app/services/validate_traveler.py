def validate_traveler(data):
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return {
            "error": "INVALID_REQUEST",
            "message": "name and email are required."
        }

    return None