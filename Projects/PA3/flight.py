from collections.abc import MutableMapping
from random import randrange
import csv

class MapBase(MutableMapping):
    class _Item:
        __slots__ = '_key', '_value'

        def __init__(self, key, value):
            self._key = key
            self._value = value

        def __eq__(self, other):
            return self._key == other._key

        def __ne__(self, other):
            return not self == other

        def __lt__(self, other):
            return self._key < other._key


class SortedTableMap(MapBase):
    """
    Map implementation using a sorted table.
    """
    # nonpublic behaviors
    def _find_index(self, k, low, high):
        """
        Return index of the leftmost item with key greater than or equal to k.
        Return high + 1 if no such item qualifies.
        That is, j will be returned such that:
            all items of slice table[low:j] have key < k
            all items of slice table[j:high+1] have key >= k
        """
        if high < low:
            # no element qualifies
            return high + 1
        else:
            mid = (low + high) // 2
            if k == self._table[mid]._key:
                # found exact match
                return mid
            elif k < self._table[mid]._key:
                # note: may return mid
                return self._find_index(k, low, mid - 1)
            else:
                # answer is right of mid
                return self._find_index(k, mid + 1, high)

    # public behaviors
    def __init__(self):
        """
        Create an empty map.
        """
        self._table = []

    def __len__(self):
        """
        Return number of items in the map.
        """
        return len(self._table)

    def __getitem__(self, k):
        """
        Return value associated with key k (raise KeyError if not found).
        """
        j = self._find_index(k, 0, len(self._table) - 1)
        if j == len(self._table) or self._table[j]._key != k:
            raise KeyError('Key Error:' + repr(k))
        return self._table[j]._value

    def __setitem__(self, k, v):
        """
        Assign value v to key k, overwriting existing value if present.
        """
        j = self._find_index(k, 0, len(self._table) - 1)
        if j < len(self._table) and self._table[j]._key == k:
            # reassign value
            self._table[j]._value = v
        else:
            # adds new item
            self._table.insert(j, self._Item(k, v))

    def __delitem__(self, k):
        """
        Remove item associated with key k (raise KeyError if not found).
        """
        j = self._find_index(k, 0, len(self._table) - 1)
        if j == len(self._table) or self._table[j]._key != k:
            raise KeyError('Key Error: ' + repr(k))
        # delete item
        self._table.pop(j)

    def __iter__(self):
        """
        Generate keys of the map ordered from minimum to maximum.
        """
        for item in self._table:
            yield item._key

    def __reversed__(self):
        """
        Generate keys of the map ordered from maximum to minimum.
        """
        for item in reversed(self._table):
            yield item._key

    def find_min(self):
        """
        Return (key, value) pair with minimum key (or None if empty).
        """
        if len(self._table) > 0:
            return (self._table[0]._key, self._table[0]._value)
        else:
            return None

    def find_max(self):
        """
        Return (key, value) pair with maximum key (or None if empty).
        """
        if len(self._table) > 0:
            return (self._table[-1]._key, self._table[-1]._value)
        else:
            return None

    def find_ge(self, k):
        """
        Return (key, value) pair with least key greater than or equal to k.
        """
        # j's key >= k
        j = self._find_index(k, 0, len(self._table) - 1)
        if j < len(self._table):
            return (self._table[j]._key, self._table[j]._value)
        else:
            return None

    def find_lt(self, k):
        """
        Return (key, value) pair with greatest key strictly less than k.
        """
        # j's key >= k
        j = self._find_index(k, 0, len(self._table) - 1)
        if j > 0:
            # note use of j-1
            return (self._table[j - 1]._key, self._table[j - 1]._value)
        else:
            return None

    def find_gt(self, k):
        """
        Return (key, value) pair with least key strictly greater than k.
        """
        # j's key >= k
        j = self._find_index(k, 0, len(self._table) - 1)
        if j < len(self._table) and self._table[j]._key == k:
            # advanced past match
            j += 1
        if j < len(self._table):
            return (self._table[j]._key, self._table[j]._value)
        else:
            return None

    def find_range(self, start, stop):
        """
        Iterate all (key, value) pairs such that start <= key <= stop.
        If start is None, iteration begins with minimum key of map.
        If stop is None, iteration continues through the maximum key of map.
        """
        if start is None:
            j = 0
        else:
            # find first result
            j = self._find_index(start, 0, len(self._table) - 1)
        while j < len(self._table) and (stop is None or self._table[j]._key < stop):
            yield (self._table[j]._key, self._table[j]._value)
            j += 1


from datetime import datetime

from datetime import datetime, timedelta

class Flight:
    def __init__(self,origin,destination,date,time,flight_number,seats_first,seats_coach,duration,fare):
        """
          Constructor for the Flight class.

          Parameters:
          - origin: The origin airport code.
          - destination: The destination airport code.
          - date: The date of the flight.
          - time: The departure time of the flight.
          - flight_number: The unique identifier for the flight.
          - seats_first: The number of available seats in the first-class section.
          - seats_coach: The number of available seats in the coach class section.
          - duration: The duration of the flight in the format 'XhYm' (hours and minutes).
          - fare: The fare for the flight.
          """
        self.origin = origin
        self.destination = destination
        self.date = date
        self.time = time
        self.flight_number = flight_number
        self.seats_first = seats_first
        self.seats_coach = seats_coach
        self.duration = self.duration_represent(duration)
        self.fare = fare
    
    def duration_represent(self,duration):
        hours, minutes = map(int,duration[:-1].split('h'))
        return timedelta(hours = hours, minutes = minutes)

    def __lt__(self, other):
        """
            Comparison method for sorting flights.

            Defines the less-than comparison based on origin, destination, date, and time.

            Parameters:
            - other: Another Flight object for comparison.
        """
        if self.origin != other.origin:
            return self.origin < other.origin
        if self.destination != other.destination:
            return self.destination < other.destination
        if self.date != other.date:
            return self.date < other.date
        
        self_time = tuple(map(int, self.time.split(':')))
        other_time = tuple(map(int, other.time.split(':')))
        return self_time < other_time


    def check_seat_availability(self, class_type):
        """
            Checks the availability of seats for a given class type.

            Parameters:
            - class_type: A string indicating the class type ('first' or 'coach').

            Returns:
            - The number of available seats for the specified class type, or None if the class type is invalid.
            """
        if class_type == 'first':
            return int(self.seats_first)
        elif class_type == 'coach':
            return int(self.seats_coach)
        else:
            return None
    

    def book_seat(self, class_type):
        """
        Books a seat for the given class type.

        Parameters:
        - class_type: A string indicating the class type ('first' or 'coach').

        Returns:
        - True if booking is successful, False otherwise.
        """
        if class_type == 'first' and int(self.seats_first) > 0:
            self.seats_first = str(int(self.seats_first) - 1)
            return True
        elif class_type == 'coach' and int(self.seats_coach) > 0:
            self.seats_coach = str(int(self.seats_coach) - 1)
            return True
        else:
            return False

    def cancel_booking(self, class_type):
        """
        Books a seat for the given class type.

        Parameters:
        - class_type: A string indicating the class type ('first' or 'coach').

        Returns:
        - True if booking is successful, False otherwise.
        """
        if class_type == 'first':
            self.seats_first = str(int(self.seats_first) + 1)
            return True
        elif class_type == 'coach':
            self.seats_coach = str(int(self.seats_coach) + 1)
            return True
        else: 
            return False

    def calculate_flight_duration(self):
        """
         Calculates the total duration of the flight.

         Returns:
         - A timedelta object representing the flight duration.
         """
        return self.duration


class FlightDatabase:
    def __init__(self):
        """
          Constructor for the FlightDatabase class.

          Creates a SortedTableMap to store flights.
          """
        self._flights = SortedTableMap()

    def add_flight(self, flight):
        """
        Adds a flight to the database.

        Parameters:
        - flight: A Flight object to be added to the database.
        """
        parameters = (flight.origin, flight.destination, flight.date, flight.time)
        self._flights[parameters] = flight

    def find_flights(self, origin, destination, date, time_start, time_end):
        """
        Finds flights within a given range of times.

        Parameters:
        - origin: The origin airport code.
        - destination: The destination airport code.
        - date: The date of the flights.
        - time_start: The start time of the range.
        - time_end: The end time of the range.

        Yields:
        - Flight objects within the specified time range.
        """
        for flight in self._flights.find_range(
            (origin, destination, date, time_start),
            (origin,destination, date, time_end)):
            yield flight

    def display_all_flights(self):
        """
             Displays all flights in the database.
             """
        print("All Flights in the Database:")
        for flight in self._flights.values():
            print(flight.origin, flight.destination, flight.date, flight.time)

    def read_flights_from_file(self, filename):
        """
        Reads flights from a CSV file and adds them to the database.

        Parameters:
        - filename: The name of the CSV file containing flight information.
        """
        with open(filename, 'r') as input_file:
            data = csv.reader(input_file)
            for row in data:
                flight = Flight(*row)
                self.add_flight(flight)

    def check_seat_availability(self, origin, destination, date, time, class_type):
        """
         Checks seat availability for a specific flight and class type.

         Parameters:
         - origin: The origin airport code.
         - destination: The destination airport code.
         - date: The date of the flight.
         - time: The departure time of the flight.
         - class_type: A string indicating the class type ('first' or 'coach').

         Returns:
         - The number of available seats for the specified class type, or None if the flight is not found.
         """
        parameters = (origin, destination, date, time)
        if parameters in self._flights:
            return self._flights[parameters].check_seat_availability(class_type)
        else: 
            return None

    def book_seat(self, origin, destination, date, time, class_type):
        """
         Books a seat for a specific flight and class type.

         Parameters:
         - origin: The origin airport code.
         - destination: The destination airport code.
         - date: The date of the flight.
         - time: The departure time of the flight.
         - class_type: A string indicating the class type ('first' or 'coach').

         Returns:
         - True if booking is successful, False otherwise.
         """
        parameters = (origin, destination, date, time)
        if parameters in self._flights:
            return self._flights[parameters].book_seat(class_type)
        else:
            return False
        
    def cancel_booking(self, origin, destination, date, time, class_type):
        """
        Cancels a booking for a specific flight and class type.

        Parameters:
        - origin: The origin airport code.
        - destination: The destination airport code.
        - date: The date of the flight.
        - time: The departure time of the flight.
        - class_type: A string indicating the class type ('first' or 'coach').

        Returns:
        - True if cancellation is successful, False otherwise.
        """
        parameters = (origin, destination, date, time)
        if parameters in self._flights:
            return self._flights[parameters].cancel_booking(class_type)
        else:
            return False

    def calculate_flight_duration(self, origin, destination, date, time):
        """
           Calculates flight duration for a specific flight.

           Parameters:
           - origin: The origin airport code.
           - destination: The destination airport code.
           - date: The date of the flight.
           - time: The departure time of the flight.

           Returns:
           - A timedelta object representing the flight duration, or None if the flight is not found.
           """
        parameters = (origin, destination, date, time)
        if parameters in self._flights:
            return self._flights[parameters].calculate_flight_duration()
        else:
            return None
        
