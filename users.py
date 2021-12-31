from utils import Utils

class User:
    is_logged_in = False

    def __init__(self, username, mobile, email, password):
        self.username = username
        self.mobile = mobile
        self.email = email
        self.password = password    # TODO: store hashed passwords instead of plaintext

    def authenticate(self, password):
        self.is_logged_in = self.password == password
        return self.is_logged_in

    def __eq__(self, __o):
        return self.username == __o.username

    def __str__(self):
        return f'Username: {self.username}\nMobile: {self.mobile}\nEmail: {self.email}'

class Passenger(User):
    def __init__(self, username, mobile, email, password):
        super().__init__(username, mobile, email, password)
        self.rides_history = []
        self.offers_history = []

    def add_ride(self, ride):
        self.rides_history.append(ride)

    def notify_offer(self, offer):
        Utils.print_header('New Offer Available')
        print(offer)

    def add_offer(self, offer):
        self.offers_history.append(offer)

class Driver(User):

    def __init__(self, username, mobile, email, password, driving_license):
        super().__init__(username, mobile, email, password)
        self.driving_license = driving_license
        self.verified = False
        self.balance = 0
        self.favorite_areas = []
        self.accepted_offers = []
        self.rides_history = []

    def is_verified(self):
        return self.verified

    def verify(self):
        self.verified = True

    def add_favorite_area(self, area):
        self.favorite_areas.append(area)
        area.register_driver(self)

    def print_favorite_areas(self):
        Utils.print_header('Favorite Areas')
        for i, favorite_area in enumerate(self.favorite_areas):
            print(f'{i+1}. {favorite_area}')

    def notify_ride(self, ride):
        Utils.print_header('New Ride Available')
        print(ride)

    def add_ended_ride(self, ride):
        self.rides_history.append(ride)
        price = ride.accepted_offer.price
        self.balance += price

    def notify_accepted_offer(self, offer):
        Utils.print_header('Offer Accepted')
        self.accepted_offers.append(offer)
        print(offer)

    def __str__(self):
        return f'{super().__str__()}\n{self.driving_license}'


class DrivingLicense:
    def __init__(self, unit, address, nationality, national_id, car_class):
        self.unit = unit
        self.address = address
        self.nationality = nationality
        self.national_id = national_id
        self.car_class = car_class

    def __str__(self):
        return f'Unit: {self.unit}\nAddress: {self.address}\nNationality: {self.nationality}\nNational ID: {self.national_id}\nCar Class: {self.car_class}'

