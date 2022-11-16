from PathPoint import CentralPoint
from Jump import Jump
from PathPoint import PathPoint

class DARTParser(object):
    @staticmethod
    def parse(content, num, plotData, points, arr):
        for i in content.split('\n'):
            if not i == "":
                splitData = i.split(' ')
                firstPoint = CentralPoint(float(splitData[0]), float(splitData[1]), num)
                num = num + 1
                secondPoint = CentralPoint(float(splitData[2]), float(splitData[3]), num)
                time = int(splitData[4])
                pauseTime = int(splitData[5])
                
                d = PathPoint.distanceInMetersBetweenEarthCoordinates(firstPoint.latitude, firstPoint.longitude, secondPoint.latitude, secondPoint.longitude)
                #if d > 5000:
                #    d = 0

                if len(plotData) == 0:
                    plotData.append(firstPoint)
                    points.append(firstPoint)
                plotData.append(secondPoint)
                points.append(secondPoint)

                jump = Jump(firstPoint, secondPoint, time, pauseTime)
                arr.append(jump)

        return num


