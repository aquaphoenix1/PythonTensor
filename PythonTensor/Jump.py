from PathPoint import CentralPoint
import json

class Jump(object):
    def __init__(self, departurePoint, destination, time, pauseTime):
        self.departurePoint = departurePoint
        self.destination = destination
        self.time = time
        self.pauseTime = pauseTime

    def to_dict(obj):
        dict = {
        "departurePoint": json.dumps(obj.departurePoint, ensure_ascii=False, default=CentralPoint.serialize),
        "destination": json.dumps(obj.destination, ensure_ascii=False, default=CentralPoint.serialize),
        "time": obj.time,
        "pauseTime": obj.pauseTime
      }
        return dict

    def hook(obj):
        return Jump(json.loads(obj['departurePoint'], object_hook=CentralPoint.deserialize), 
                    json.loads(obj['destination'], object_hook=CentralPoint.deserialize),
                    obj['time'],
                    obj['pauseTime'])