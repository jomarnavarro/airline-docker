import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Flight(db.Model):
    __tablename__ = "flights"
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    passengers = db.relationship("Passenger", backref="flight", lazy=True)

    def __init__(self, flight_origin, flight_destination, flight_duration):
        self.origin = flight_origin
        self.destination = flight_destination
        self.duration = flight_duration

    def add_passenger(self, name):
        p = Passenger(name=name, flight_id=self.id)
        db.session.add(p)
        db.session.commit()
        db.session.refresh(p)
        return p.id

    def add_flight(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)
        return self.id


class Passenger(db.Model):
    __tablename__ = "passengers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey("flights.id"), nullable=False)
