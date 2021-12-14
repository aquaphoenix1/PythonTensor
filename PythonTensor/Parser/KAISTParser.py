from PathPoint import CentralPoint
from Jump import Jump

class KAISTParser(object):
    @staticmethod
    def parse(content, num, plotData, points, arr):
        c = content.split('\n')
        for i in range(len(c) - 1):
            if c[i+1]== "":
                break;
            splitData = c[i].split('\t')
            for k in range(len(splitData)):
                splitData[k] = splitData[k].strip()
            time1 = int(float(splitData[0]))
            firstPoint = CentralPoint(float(splitData[1]), float(splitData[2]), num)
            num = num + 1
            splitData = c[i+1].split('\t')
            time2 = int(float(splitData[0]))
            secondPoint = CentralPoint(float(splitData[1]), float(splitData[2]), num)

            if len(plotData) == 0:
                plotData.append(firstPoint)
                points.append(firstPoint)
            plotData.append(secondPoint)
            points.append(secondPoint)

            jump = Jump(firstPoint, secondPoint, time2-time1, 0)

            arr.append(jump)

        return num


