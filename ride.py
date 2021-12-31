from utils import Utils
#import requests

class Offer:
    def __init__(self, ride, driver, price):
        self.ride = ride
        self.price = price
        self.driver = driver

        ride.passenger.notify_offer(self)

    def accept(self):
        self.driver.notify_accepted_offer(self)
        self.ride.assign_offer(self)
        self.ride.start()

    def __str__(self):
        return f' --------------\n| Ride Details |\n --------------\n{self.ride}\n\n' +\
               f'Price: {self.price}\n\n' +\
               f' ----------------\n| Driver Details |\n ----------------\n{self.driver}'


class Ride:
    GOOGLE_API_CALLS = 0
    GOOGLE_API_LIMIT = 2
    AVG_SPEED = 60.0
    GOOGLE_API_KEY = 'AIzaSyABl_touOteQ_JfbxodGAk89Epax3Z40P8'

    def __init__(self, passenger, source_area, destination_area):
        self.passenger = passenger
        self.source_area = source_area
        self.destination_area = destination_area
        self.offers = []
        self.state = 'Pending'
        self.accepted_offer = False
        self.rating = 'Unrated'
        self._calculate_distance_eta()

        passenger.add_ride(self)
        source_area.notify_drivers(self)

    def assign_offer(self, offer):
        self.accepted_offer = offer
        self.passenger.add_offer(self)

    def make_offer(self, driver, price):
        offer = Offer(self, driver, price)
        self.offers.append(offer)

    def get_offer_by_driver(self, driver):
        return [offer for offer in self.offers if offer.driver == driver]

    def is_pending(self):
        return self.state == 'Pending'

    def is_in_progress(self):
        return self.state == 'In-Progress'

    def is_ended(self):
        return self.state == 'Ended'

    def is_rated(self):
        return self.rating != 'Unrated'

    def start(self):
        self.state = 'In-Progress'

    def end(self):
        self.state = 'Ended'
        self.accepted_offer.driver.add_ended_ride(self)

    def rate(self, rating):
        self.rating = rating

    def _calculate_distance_eta(self):
        if Ride.GOOGLE_API_CALLS < Ride.GOOGLE_API_LIMIT:
            self._calculate_distance_google_maps()
        else:
            self._calculate_distance_eta_haversine()

        self.distance = round(self.distance, 2)
        self.eta = round(self.eta, 2)

    def _calculate_distance_eta_haversine(self):
        source_longitude, source_latitude = self.source_area.get_coordinates()
        destination_longitude, destination_latitude = self.destination_area.get_coordinates()
        self.distance = Utils.haversine(source_longitude, source_latitude, destination_longitude, destination_latitude)
        self.eta = self.distance * 60 / Ride.AVG_SPEED

    def _calculate_distance_google_maps(self):
        source_longitude, source_latitude = self.source_area.get_coordinates()
        destination_longitude, destination_latitude = self.destination_area.get_coordinates()

        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={source_latitude}%2C{source_longitude}&destinations=side_of_road%3A{destination_latitude}%2C{destination_longitude}&key={Ride.GOOGLE_API_KEY}"
        response = requests.request("GET", url)
        response_json = response.json()
        status = response_json['status']
        rows = response_json['rows']
        if status == 'OK' and rows:
            element = rows[0]['elements'][0]
            self.distance = element['distance']['value'] / 1000 # Convert to KM
            self.eta = element['duration_in_traffic']['value'] / 60 # Convert to Mins
        else:
            # Fallback to haversine calculation
            self._calculate_distance_eta_haversine()
        Ride.GOOGLE_API_CALLS += 1

    def __str__(self):
        return f'Source Area: {self.source_area}\nDestination Area: {self.destination_area}\nState: {self.state}\nDistance: {self.distance} KM\nETA: {self.eta} Minutes\n\nRating: {self.rating}'

