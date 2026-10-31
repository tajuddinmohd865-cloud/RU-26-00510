"""Flight Booking Management System (PS No. 73)
Concepts: OOP, CSV, Lists, Functions
"""
import csv

CSV_FILE = "flights.csv"


class Flight:
    def __init__(self, flight_no, origin, destination, seats, fare):
        self.flight_no = flight_no
        self.origin = origin
        self.destination = destination
        self.seats = int(seats)
        self.fare = int(fare)

    def book(self, count):
        """Reduce seats. Returns (ok, message)."""
        if count < 1:
            return False, "Number of seats must be at least 1."
        if self.seats == 0:
            return False, f"Flight {self.flight_no} is full."
        if count > self.seats:
            return False, f"Only {self.seats} seat(s) available on {self.flight_no}."
        self.seats -= count
        return True, ""

    def cancel(self, count):
        """Give seats back."""
        self.seats += count

    def __str__(self):
        return (f"{self.flight_no} | {self.origin} -> {self.destination} | "
                f"Seats: {self.seats} | Fare: Rs. {self.fare} per seat")


class Booking:
    def __init__(self, booking_id, passenger, flight, seats):
        self.booking_id = booking_id
        self.passenger = passenger
        self.flight = flight
        self.seats = seats
        self.total = seats * flight.fare


def load_flights(filename):
    """Read flights.csv into a list of Flight objects."""
    flights = []
    try:
        with open(filename, newline="") as f:
            for row in csv.DictReader(f):
                flights.append(Flight(row["FlightNo"].strip(),
                                      row["Origin"].strip(),
                                      row["Destination"].strip(),
                                      row["Seats"], row["Fare"]))
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    return flights


def search_flights(flights, origin, destination):
    """Case-insensitive search by origin and destination."""
    return [f for f in flights
            if f.origin.lower() == origin.strip().lower()
            and f.destination.lower() == destination.strip().lower()]


def find_flight(flights, flight_no):
    for f in flights:
        if f.flight_no.lower() == flight_no.strip().lower():
            return f
    return None


def book_ticket(flights, bookings, flight_no, passenger, seats):
    flight = find_flight(flights, flight_no)
    if flight is None:
        print(f"Flight {flight_no} not found.")
        return
    ok, msg = flight.book(seats)
    if not ok:
        print(msg)
        return
    booking = Booking(f"BK{len(bookings) + 1}", passenger, flight, seats)
    bookings.append(booking)
    print(f"Booking confirmed. ID: {booking.booking_id} | {passenger} | "
          f"{flight.flight_no} | {seats} seat(s) | "
          f"Total: Rs. {booking.total} | Seats left: {flight.seats}")


def cancel_booking(bookings, booking_id):
    for b in bookings:
        if b.booking_id.lower() == booking_id.strip().lower():
            b.flight.cancel(b.seats)
            bookings.remove(b)
            print(f"Booking {b.booking_id} cancelled. "
                  f"Seats left on {b.flight.flight_no}: {b.flight.seats}")
            return
    print(f"Booking {booking_id} not found.")


def read_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        return 0  # treated as invalid -> "at least 1" message


def main():
    flights = load_flights(CSV_FILE)
    if not flights:
        return
    bookings = []
    while True:
        print("\n1. Search flights\n2. Book\n3. Cancel booking\n4. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            origin = input("Origin: ")
            dest = input("Destination: ")
            results = search_flights(flights, origin, dest)
            if results:
                for f in results:
                    print(f)
            else:
                print("No flights found.")
        elif choice == "2":
            fno = input("Flight: ")
            name = input("Passenger: ")
            seats = read_int("Seats: ")
            book_ticket(flights, bookings, fno, name, seats)
        elif choice == "3":
            cancel_booking(bookings, input("Booking ID: "))
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
