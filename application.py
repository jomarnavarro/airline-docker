import requests
from flask import Flask, render_template, jsonify, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def index():
    flights = Flight.query.all()
    return render_template("index.html", flights=flights)


@app.route("/book", methods=["POST"])
def book():
    """Book a flight."""

    # Get form information.
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Invalid flight number.")

    # Make sure the flight exists.
    flight = Flight.query.get(flight_id)
    if not flight:
        return render_template("error.html", message="No such flight with that id.")

    # Add passenger.
    flight.add_passenger(name)
    return render_template("success.html")


@app.route("/flights")
def flights():
    """List all flights."""
    flights = Flight.query.all()
    return render_template("flights.html", flights=flights)


@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    """List details about a single flight."""

    # flight_info = flight_api(flight_id).json
    flight_info = requests.get(f"http://localhost:5000/api/flights/{flight_id}").json()
    if "error" in flight_info:

        return render_template("error.html", message="No such flight.")
    return render_template("flight.html", flight=flight_info, passengers=flight_info['passengers'])
    # # Make sure flight exists.
    # flight = Flight.query.get(flight_id)
    # if flight is None:
    #     return render_template("error.html", message="No such flight.")
    #
    # # Get all passengers.
    # passengers = flight.passengers
    # return render_template("flight.html", flight=flight, passengers=passengers)

@app.route("/api/flights/", methods=['GET'])
def flight_api_no_flight_id():
    return jsonify({"error": "No flight id was specified."}), 500

@app.route("/api/flights/<int:flight_id>", methods=['GET'])
def flight_api(flight_id):
    """Return details about a single flight."""
    if check_int_data_type(flight_id) != 0:
        return jsonify({"error", "flight_id is in wrong format."}), 500
    # Make sure flight exists.
    flight = Flight.query.get(flight_id)
    if flight is None:
        return jsonify({"error": "Invalid flight_id"}), 422

    # Get all passengers.
    passengers = flight.passengers
    names = []
    for passenger in passengers:
        names.append(passenger.name)
    return jsonify({
            "origin": flight.origin,
            "destination": flight.destination,
            "duration": flight.duration,
            "passengers": names
        })

def check_string_data_type(string_data):
    print('Hello world!')
    print(string_data)
    print(isinstance(string_data, type(str)))
    if isinstance(string_data, type(str)):
        return 1
    if string_data == '':
        return 1
    try:
        integ = int(string_data)
        return 1
    except:
        return 0
    return 0

def check_int_data_type(int_data):
    if isinstance(int_data, type(int)):
        return 0
    try:
        integ = int(int_data)
        return 0
    except:
        return 1


@app.route("/api/reservations/<int:reservation_id>", methods=['GET'])
def reservations_api(reservation_id):
    """Return details about a reservation flight."""
    # make sure reservation_id has the correct data type
    if check_int_data_type(reservation_id) != 0:
        return jsonify({"error", "reservation_id is in wrong format."}), 500
    
    # Make sure flight exists.
    reservation = Passenger.query.get(reservation_id)

    if reservation is None:
        return jsonify({"error": "Invalid reservation_id"}), 422

    flight_info = Flight.query.get(reservation.flight_id)

    if flight_info is None:
        return jsonify({"error": "Invalid flight_id: {reservation.flight_id}"}), 422
    # return flight reservation info
    return jsonify({
            "origin": flight_info.origin,
            "destination": flight_info.destination,
            "duration": flight_info.duration,
            "passenger": reservation.name,
            "reservation_id": reservation.id
        })

@app.route("/api/reservation/new", methods=['POST'])
def api_book_flight():
    name = request.json['name']
    if check_string_data_type(name) == 1:
        return jsonify({"error": "Passenger name is invalid"}), 400
    flight_id = request.json['flight_id']
    if check_int_data_type(flight_id) == 1:
        return jsonify({"error": "Flight id is invalid"}), 400
    #Make sure the flight exists
    flight = Flight.query.get(flight_id)
    if not flight:
        return jsonify({"error": "No such flight id"})
    reservation_id = flight.add_passenger(name)

    return jsonify({
            "origin": flight.origin,
            "destination": flight.destination,
            "duration": flight.duration,
            "name": name,
            "reservation_id": reservation_id
    })

@app.route("/api/flight/new", methods=["POST"])
def api_create_flight():
    origin = request.json['origin']
    if check_string_data_type(origin) == 1:
        return jsonify({"error": "Origin is invalid"}), 400
    
    destination = request.json['destination']
    if check_string_data_type(destination) == 1:
        return jsonify({"error": "Destination is invalid"}), 400
    
    duration = int(request.json['duration'])
    if check_int_data_type(duration) == 1:
        return jsonify({"error": "Duration is invalid"}), 400
    
    flight = Flight(origin, destination, duration)
    flight_id = flight.add_flight()

    return jsonify({
        "flight_id": flight_id,
        "origin": origin,
        "destination": destination,
        "duration": duration
    })