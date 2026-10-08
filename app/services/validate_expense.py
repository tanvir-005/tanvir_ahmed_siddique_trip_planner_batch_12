def validate_expense(data):
    title = data.get("title")
    amount = data.get("amount")

    if not title or amount is None:
        return {
            "error": "INVALID_REQUEST",
            "message": "title and amount are required."
        }

    if not isinstance(amount, (int, float)):
        return {
            "error": "INVALID_AMOUNT",
            "message": "amount must be a number."
        }

    if amount <= 0:
        return {
            "error": "INVALID_AMOUNT",
            "message": "amount must be greater than zero."
        }

    # no error means all ok
    return None