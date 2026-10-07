def trip_summary(trip):
    total_expenses = sum(
        expense.amount
        for expense in trip.expenses
    )

    expenses = [
        {
            "id": expense.id,
            "title": expense.title,
            "amount": expense.amount
        }
        for expense in trip.expenses
    ]

    return {
        "id": trip.id,
        "destination": trip.destination,
        "start_date": trip.start_date.isoformat(),
        "end_date": trip.end_date.isoformat(),
        "status": trip.status,
        "travelers": len(trip.travelers),
        "max_travelers": trip.max_travelers,
        "budget": trip.budget,
        "total_expenses": total_expenses,
        "remaining_budget": trip.budget - total_expenses,
        "expenses": expenses
    }