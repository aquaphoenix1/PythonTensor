class Point(object):
    def __init__(self, date, altitude, latitude, longitude, hdop, speed):
        self.date = date
        self.altitude = altitude
        self.latitude = latitude
        self.longitude = longitude
        self.hdop = hdop
        self.speed = speed

    def serialize(obj):
        return{
            "date": obj.date,
            "latitude": obj.latitude,
            "longitude": obj.longitude
            }

    def deserialize(i):
        return Point(i["date"], 0, i["latitude"], i["longitude"], 0, 0)