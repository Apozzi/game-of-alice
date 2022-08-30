import math
from point import Point

class Line:
    def __init__(self, lineTuple):
        self.start_point = Point(lineTuple[0])
        self.end_point = Point(lineTuple[1])

    def getStartPoint(self):
        return self.start_point

    def getEndPoint(self):
        return self.end_point

    def getMaxX(self):
        return self.start_point.x if self.start_point.x > self.end_point.x else self.end_point.x
    
    def getMinX(self):
        return self.start_point.x if self.start_point.x < self.end_point.x else self.end_point.x

    def getMaxY(self):
        return self.start_point.y if self.start_point.y > self.end_point.y else self.end_point.y
    
    def getMinY(self):
        return self.start_point.y if self.start_point.y < self.end_point.y else self.end_point.y

    def __getYFromX(self, xPos):
        if self.start_point.x == xPos:
            return self.start_point.y
        if self.end_point.x == xPos:
            return self.end_point.y
        return None
    
    def isAscendingLine(self):
        return self.__getYFromX(self.getMinX()) < self.__getYFromX(self.getMaxX())

    def isDescendingLine(self):
        return self.__getYFromX(self.getMinX())  > self.__getYFromX(self.getMaxX())

    def continuityBetween(self, otherLine):
        line1StartCoont = self.start_point == otherLine.start_point or self.start_point == otherLine.end_point
        line1EndCoont = self.end_point == otherLine.start_point or self.end_point == otherLine.end_point
        return line1StartCoont or line1EndCoont

    def getAngle(self):
        xSize = self.getMaxX() - self.getMinX()
        ySize = self.getMaxY() - self.getMinY()
        return math.atan2(ySize, xSize)
