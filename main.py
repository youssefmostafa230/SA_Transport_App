from api import AdminAPI, DriverAPI, PassengerAPI
from users import Driver, Passenger
from utils import Utils

class App(AdminAPI, DriverAPI, PassengerAPI):
    def start(self):
        while True:
            if not self.logged_in_user and not self._show_main_menu():
                break
            elif self.logged_in_user:
                if self.is_admin:
                    self._show_admin_menu()
                elif isinstance(self.logged_in_user, Driver):
                    self._show_driver_menu()
                elif isinstance(self.logged_in_user, Passenger):
                    self._show_passenger_menu()

    def _show_login_screen(self):
        Utils.print_header('Login')
        username = input('Username: ')
        password = input('Password: ')
        self._login(username, password)

    def _show_signup_screen(self):
        Utils.print_header('Signup')
        print('''
        1. Driver Signup
        2. Passenger Signup
        3. Back
        ''')
        choice = input('Your choice: ')
        if choice == '1':
            self._show_driver_signup_screen()
        elif choice == '2':
            self._show_passenger_signup_screen()

    def _show_main_menu(self):
        Utils.print_header('Welcome To Ride Booking!')

        print('''
        1. Login
        2. Signup
        3. Exit''')

        choice = input('Your choice: ')

        if choice == '1':
            self._show_login_screen()
        elif choice == '2':
            self._show_signup_screen()
        elif choice == '3':
            return False
        else:
            Utils.print_error('Invalid choice!')
        return True


app = App()
app.start()