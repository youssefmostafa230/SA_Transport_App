from area import Area
from ride import Ride
from users import Driver, DrivingLicense, Passenger, User
from utils import Utils

class BaseAPI:
    areas_dict = {}
    rides = []

    logged_in_user = False

    def _get_area_object(self, area_str):
        normalized_area_str = area_str.lower().replace(' ', '_')
        if not self.areas_dict.get(normalized_area_str):
            print('New Area Coordinates')
            longitude = float(input('Longitude: '))
            latitude = float(input('Latitude: '))
            self.areas_dict[normalized_area_str] = Area(area_str, longitude, latitude)
        return self.areas_dict[normalized_area_str]

    def _read_common_signup_data(self):
        username = input('Username: ')
        while self.drivers_dict.get(username) or self.passengers_dict.get(username) or self.admins_dict.get(username):
            Utils.print_error('This username is already registered!')
            username = input('Username: ')
        mobile = input('Mobile: ')
        email = input('Email: ')

        password = input('Password: ')
        confirm_password = input('Confirm Password: ')
        while password != confirm_password:
            Utils.print_error('Passwords do not match!')
            password = input('Password: ')
            confirm_password = input('Confirm Password: ')
        return username, mobile, email, password

    def _login(self, username, password):
        Utils.print_error('This username is not registered!')
        return False


class AdminAPI(BaseAPI):
    admins_dict = {}
    is_admin = False

    def __init__(self):
        self.admins_dict['admin'] = User('admin', False, False, 'admin')

    def _verify_pending_drivers(self):
        Utils.print_header('Drivers Verification')

        pending_drivers = [driver for driver in self.drivers_dict.values() if not driver.is_verified()]

        if len(pending_drivers) == 0:
            print('There are no pending drivers.')
            return

        for i, driver in enumerate(pending_drivers):
            print(f'{i}.\t{driver}')

        index = int(input('Your choice: '))
        if index < len(pending_drivers):
            pending_drivers[index].verify()

    def _show_all_drivers(self):
        Utils.print_header('Drivers List')
        for driver in self.drivers_dict.values():
            print(driver)

    def _show_all_passengers(self):
        Utils.print_header('Passengers List')
        for passenger in self.passengers_dict.values():
            print(passenger)

    def _show_admin_menu(self):
        Utils.print_header('Admin Menu')
        print('''
        1. Show All Drivers
        2. Show All Passengers
        3. Verify Pending Drivers
        4. Logout
        ''')

        choice = input('Your choice: ')
        if choice == '1':
            self._show_all_drivers()
        elif choice == '2':
            self._show_all_passengers()
        elif choice == '3':
            self._verify_pending_drivers()
        elif choice == '4':
            self.logged_in_user = False
            self.is_admin = False
        else:
            Utils.print_error('Invalid choice!')

    def _login(self, username, password):
        admin = self.admins_dict.get(username)

        if admin and admin.authenticate(password):
            self.logged_in_user = admin
            self.is_admin = True
            return True
        return super()._login(username, password)


class DriverAPI(BaseAPI):
    drivers_dict = {}

    def _get_driver_favorite_rides(self, pending_only=True):
        return [r for r in self.rides if r.source_area in self.logged_in_user.favorite_areas and (not pending_only or (pending_only and r.is_pending()))]

    def _make_offer(self):
        Utils.print_header('Make An Offer')
        print('Select a ride...')
        favorite_rides = self._get_driver_favorite_rides()

        if len(favorite_rides) == 0:
            print('No rides available.')
            return

        for i, ride in enumerate(favorite_rides):
            print (f'{i}. {ride}')

        choice = int(input('Your choice: '))
        if choice > len(favorite_rides) or choice < 0:
            Utils.print_error('Invalid choice!')
            return

        ride = favorite_rides[choice]
        price = float(input('Offer Price: '))
        ride.make_offer(self.logged_in_user, price)

    def _print_driver_rides(self):
        Utils.print_header('Favorite Areas Rides')
        favorite_rides = self._get_driver_favorite_rides()
        for ride in favorite_rides:
            print(ride)
            Utils.print_separator()

    def _add_driver_favorite_area(self):
        favorite_area = input('Favorite Area: ')
        favorite_area = self._get_area_object(favorite_area)
        self.logged_in_user.add_favorite_area(favorite_area)

    def _get_driver_offers(self):
        offers = []
        favorite_rides = self._get_driver_favorite_rides()
        for ride in favorite_rides:
            offers += ride.get_offer_by_driver(self.logged_in_user)
        return offers

    def _print_my_offers(self):
        Utils.print_header('My Pending Rides Offers')
        for offer in self._get_driver_offers():
            print(offer)
            Utils.print_separator()

    def _print_rides_history(self):
        Utils.print_header('Rides History')
        for ride in self.logged_in_user.rides_history:
            print(ride)
            Utils.print_separator()

    def _print_balance(self):
        Utils.print_header('My Balance')
        balance = self.logged_in_user.balance
        print(f'Balance: {balance}')

    def _end_ride(self):
        Utils.print_header('End A Ride')
        in_progress_rides = [offer.ride for offer in self.logged_in_user.accepted_offers if offer.ride.is_in_progress()]
        for i, ride in enumerate(in_progress_rides):
            print(f'{i}. {ride}')
            Utils.print_separator()

        if not in_progress_rides:
            print('No rides in-progress.')
            return

        choice = int(input('Your choice: '))
        if choice > len(in_progress_rides) or choice < 0:
            Utils.print_error('Invalid choice!')
            return

        in_progress_rides[choice].end()

    def _show_driver_menu(self):
        Utils.print_header('Driver Menu')
        print('''
        1. Show Favorite Areas
        2. Add A Favorite Area
        3. Favorite Area Rides
        4. My Pending Rides Offers
        5. Make An Offer
        6. End A Ride
        7. Rides History
        8. My Balance
        9. Logout
        ''')

        choice = input('Your choice: ')
        if choice == '1':
            self.logged_in_user.print_favorite_areas()
        elif choice == '2':
            self._add_driver_favorite_area()
        elif choice == '3':
            self._print_driver_rides()
        elif choice == '4':
            self._print_my_offers()
        elif choice == '5':
            self._make_offer()
        elif choice == '6':
            self._end_ride()
        elif choice == '7':
            self._print_rides_history()
        elif choice == '8':
            self._print_balance()
        elif choice == '9':
            self.logged_in_user = False
        else:
            Utils.print_error('Invalid choice!')

    def _show_driver_signup_screen(self):
        Utils.print_header('Driver Registration')

        username, mobile, email, password = self._read_common_signup_data()

        unit = input('Unit: ')
        address = input('Address: ')
        nationality = input('Nationality: ')
        national_id = input('National ID: ')
        car_class = input('Car Class: ')

        driving_license = DrivingLicense(unit, address, nationality, national_id, car_class)
        self.drivers_dict[username] = Driver(username, mobile, email, password, driving_license)

    def _login(self, username, password):
        driver = self.drivers_dict.get(username)

        if driver and driver.is_verified() and driver.authenticate(password):
            self.logged_in_user = driver
            return True
        return super()._login(username, password)


class PassengerAPI(BaseAPI):
    passengers_dict = {}

    def _request_ride(self):
        Utils.print_header('Request A Ride')

        source_area = input('Source Area: ')
        destination_area = input('Destination Area: ')

        source_area = self._get_area_object(source_area)
        destination_area = self._get_area_object(destination_area)

        ride = Ride(self.logged_in_user, source_area, destination_area)
        self.rides.append(ride)

    def _print_my_rides(self):
        Utils.print_header('My Rides')
        for ride in self.logged_in_user.rides_history:
            print(ride)
            Utils.print_separator()

    def _print_my_rides_offers(self):
        Utils.print_header('My Rides Offers')
        for ride in self.logged_in_user.rides_history:
            for offer in ride.offers:
                print(offer)
                Utils.print_separator()

    def _rate_previous_rides(self):
        Utils.print_header('Rate Previous Rides')
        rides = [ride for ride in self.logged_in_user.rides_history if ride.is_ended() and not ride.is_rated()]
        for i, ride in enumerate(rides):
            print(f'{i}. {ride}')
            Utils.print_separator()

        if not rides:
            print('No rides to rate.')
            return

        choice = int(input('Your choice: '))
        if choice > len(rides) or choice < 0:
            Utils.print_error('Invalid choice!')
            return

        rating = input('Your rating: ')
        rides[choice].rate(rating)

    def _accept_offer(self):
        Utils.print_header('Accept An Offer')
        i = 0
        offers = []
        for ride in self.logged_in_user.rides_history:
            for offer in ride.offers:
                if not offer.ride.is_pending():
                    continue
                print(f'{i}.{offer}')
                offers.append(offer)
                i += 1
                Utils.print_separator()

        if not offers:
            print('No pending offers available.')
            return
        choice = int(input('Your choice: '))
        if choice > len(offers) or choice < 0:
            Utils.print_error('Invalid choice!')
            return

        offers[choice].accept()

    def _show_passenger_signup_screen(self):
        Utils.print_header('Passenger Registration')

        username, mobile, email, password = self._read_common_signup_data()
        self.passengers_dict[username] = Passenger(username, mobile, email, password)

    def _show_passenger_menu(self):
        Utils.print_header('Passenger Menu')
        print('''
        1. Request A Ride
        2. My Rides
        3. My Rides Offers
        4. Accept Offer
        5. Rate Previous Rides
        6. Logout
        ''')

        choice = input('Your choice: ')
        if choice == '1':
            self._request_ride()
        elif choice == '2':
            self._print_my_rides()
        elif choice == '3':
            self._print_my_rides_offers()
        elif choice == '4':
            self._accept_offer()
        elif choice == '5':
            self._rate_previous_rides()
        elif choice == '6':
            self.logged_in_user = False
        else:
            Utils.print_error('Invalid choice!')

    def _login(self, username, password):
        passenger = self.passengers_dict.get(username)

        if passenger and passenger.authenticate(password):
            self.logged_in_user = passenger
            return True
        return super()._login(username, password)

