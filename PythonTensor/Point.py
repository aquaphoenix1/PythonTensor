class Point(object):
    def __init__(self, date, altitude, latitude, longitude, hdop, speed):
        self.date = date
        self.altitude = altitude
        self.latitude = latitude
        self.longitude = longitude
        self.hdop = hdop
        self.speed = speed