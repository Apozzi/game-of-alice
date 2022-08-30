import math

class Point:
    def __init__(self, pointTuple):
        self.x = pointTuple[0]
        self.y = pointTuple[1]

    def __add__(self, other):
        x = self.x + other.y
        y = self.x + other.y
        return Point((x, y))
    
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point((x, y))

    def __eq__(self, other):
        x = self.x == other.x
        y = self.y == other.y
        return x and y

    def div(self, number):
        x = self.x / number
        y = self.y / number
        return Point((x, y))

    def distance(self, other):
        dx = self.x - other.x
        dy = self.x - other.y
        return math.sqrt(dx**2 + dy**2)

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def __str__(self):
        return "Point(%s,%s)"%(self.x, self.y) 
