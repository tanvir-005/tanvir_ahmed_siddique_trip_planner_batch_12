from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Integer, nullable=False)
    max_travelers = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="PLANNED")

    