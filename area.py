class Area:
    def __init__(self, name, longitude, latitude):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.registered_drivers = []

    def register_driver(self, driver):
        self.registered_drivers.append(driver)

    def notify_drivers(self, ride):
        for driver in self.registered_drivers:
            driver.notify_ride(ride)

    def get_coordinates(self):
        return self.longitude, self.latitude

    def __str__(self):
        return self.name

    def __eq__(self, __o):
        return self.name == __o.name

