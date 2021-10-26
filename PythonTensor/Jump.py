class Jump(object):
    departurePoint = None
    destination = None
    time = None
    pauseTime = None

    def __init__(self, departurePoint, destination, time, pauseTime):
        self.departurePoint = departurePoint
        self.destination = destination
        self.time = time
        self.pauseTime = pauseTime