from math import radians, cos, sin, asin, sqrt

class Utils:
    @classmethod
    def print_header(cls, title):
        extra_asterisk_count = 7
        full_asterisk_count = len(title) + (extra_asterisk_count + 1) * 2
        half_asterisk_count = int((full_asterisk_count - len(title) - 2) / 2)
        print('')
        print('*' * full_asterisk_count)
        print('*' * full_asterisk_count)
        print('*' * half_asterisk_count + f' {title} ' + '*' * half_asterisk_count)
        print('*' * full_asterisk_count)
        print('*' * full_asterisk_count)
        print('')

    @classmethod
    def print_error(cls, message):
        print('')
        print(f'Error:\n\t{message}')
        print('')

    @classmethod
    def print_separator(cls):
        print('=' * 50)

    @classmethod
    def haversine(cls, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance in kilometers between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
        return c * r