class Jump(object):
    departurePoint = None
    destination = None
    time = None

    def __init__(self, departurePoint, destination, time):
        self.departurePoint = departurePoint
        self.destination = destination
        self.time = time