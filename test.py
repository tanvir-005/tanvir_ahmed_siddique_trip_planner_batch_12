import unittest
from datetime import date

from app.services import validate_trip, validate_change, trip_dictonarize, validate_traveler, validate_trip_join, validate_expense, validate_status_change, trip_summary, validate_status_on_trip_creation

from app.models import Trip, Traveler, Expense


class TestAll(unittest.TestCase):
    def test_valid_trip_data(self):
        data = {
            "destination": "Kuakata",
            "start_date": "2026-10-09",
            "end_date": "2026-10-11",
            "budget": 15000,
            "max_travelers": 5,
        }
        # assert function will check whether validate_trip() returns any error not
        self.assertIsNone(validate_trip(data))

    def test_invalid_trip_data(self):
        data = {
            "destination": "Kuakata",
            "start_date": "2026-12-09",
            "end_date": "2026-10-11",
            "budget": 15000,
            "max_travelers": 5,
        }
        self.assertIsNotNone(validate_trip(data))

    def test_incomplete_trip_data(self):
        data = {
            "budget": 15000,
            "max_travelers": 5,
        }
        self.assertIsNotNone(validate_trip(data))

    def test_invalid_trip_budget(self):
        data = {
            "destination": "Kuakata",
            "start_date": "2026-10-09",
            "end_date": "2026-10-11",
            "budget": -15000,
            "max_travelers": 5,
        }
        self.assertIsNotNone(validate_trip(data))

    def test_invalid_trip_capacity(self):
        data = {
            "destination": "Kuakata",
            "start_date": "2026-10-09",
            "end_date": "2026-10-11",
            "budget": 15000,
            "max_travelers": -5,
        }
        self.assertIsNotNone(validate_trip(data))

    def test_invalid_trip_date(self):
        data = {
            "destination": "Kuakata",
            "start_date": "invalid-date",
            "end_date": "2026-10-11",
            "budget": 15000,
            "max_travelers": 5,
        }
        self.assertIsNotNone(validate_trip(data))

    def test_invalid_trip_budget_nan(self):
        data = {
            "destination": "Kuakata",
            "start_date": "2026-10-10",
            "end_date": "2026-10-11",
            "budget": "15000",
            "max_travelers": 5,
        }
        self.assertIsNotNone(validate_trip(data))

    def test_invalid_trip_capacity_nan(self):
        data = {
            "destination": "Kuakata",
            "start_date": "2026-10-10",
            "end_date": "2026-10-11",
            "budget": 15000,
            "max_travelers": "5",
        }
        self.assertIsNotNone(validate_trip(data))

    def test_valid_trip_status(self):
        data = {
            "destination": "Kuakata",
            "start_date": "2026-10-09",
            "end_date": "2026-10-11",
            "budget": 15000,
            "max_travelers": 5,
            "status": "PLANNED"
        }
        self.assertIsNone(validate_status_on_trip_creation(data["status"]))

    def test_valid_trip_status_empty(self):
        data = {
            "destination": "Kuakata",
            "start_date": "2026-10-09",
            "end_date": "2026-10-11",
            "budget": 15000,
            "max_travelers": 5,
            "status": None
        }
        self.assertIsNone(validate_status_on_trip_creation(data["status"]))

    def test_invalid_trip_status(self):
        data = {
            "destination": "Kuakata",
            "start_date": "2026-10-09",
            "end_date": "2026-10-11",
            "budget": 15000,
            "max_travelers": 5,
            "status": "ONGOING"
        }
        self.assertIsNotNone(validate_status_on_trip_creation(data["status"]))

    def test_valid_trip_join(self):
        # trip
        trip = Trip()
        trip.id = 10
        trip.destination = "Shitakunda, Chattogram"
        trip.start_date = "2026-10-10"
        trip.end_date = "2026-10-11"
        trip.budget = 6000
        trip.max_travelers = 2
        trip.status = "PLANNED"
        trip.travelers = []
        trip.expenses = []

        # traveler
        traveler = Traveler()
        traveler.id = 10
        traveler.name = "Tanvir"
        traveler.email = "tanvir@w3engineers.com"
        traveler.trips = []

        self.assertIsNone(validate_trip_join(trip, traveler))

    def test_invalid_trip_join(self):
        # trip
        trip = Trip()
        trip.id = 10
        trip.destination = "Shitakunda, Chattogram"
        trip.start_date = "2026-10-10"
        trip.end_date = "2026-10-11"
        trip.budget = 6000
        trip.max_travelers = 2
        trip.status = "PLANNED"
        trip.travelers = []
        trip.expenses = []

        # some travelers
        traveler1 = Traveler()
        traveler1.id = 10
        traveler1.name = "Tanvir"
        traveler1.email = "tanvir@w3engineers.com"
        traveler1.trips = []

        traveler2 = Traveler()
        traveler2.id = 11
        traveler2.name = "Ahmed"
        traveler2.email = "ahmed@w3engineers.com"
        traveler2.trips = []

        traveler3 = Traveler()
        traveler3.id = 10
        traveler3.name = "Siddique"
        traveler3.email = "siddique@w3engineers.com"
        traveler3.trips = []

        trip.travelers.append(traveler1)
        trip.travelers.append(traveler2)
        self.assertIsNotNone(validate_trip_join(trip, traveler3))

    def test_valid_traveler(self):
        data = {
            "name": "Tanvir",
            "email": "tanvir@example.com"
        }
        self.assertIsNone(validate_traveler(data))

    def test_invalid_traveler(self):
        data = {
            "name": "Tanvir"
        }

        result = validate_traveler(data)
        self.assertIsNotNone(result)

    def test_valid_status_change(self):
        trip = Trip()
        trip.status = "PLANNED"
        self.assertIsNone(validate_status_change(trip, "ONGOING"))

    def test_invalid_status_change(self):
        trip = Trip()
        trip.status = "ONGOING"
        self.assertIsNotNone(validate_status_change(trip, "PLANNED"))

if __name__ == "__main__":
    unittest.main()
