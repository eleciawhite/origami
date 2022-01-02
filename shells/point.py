from math import *

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def fromVertices(cls, v):
        ret = cls(v[0],v[1])
        return ret

    def lengthTo(self, p):
        x2 = (self.x-p.x)**2
        y2 = (self.y-p.y)**2
        return sqrt(x2 + y2)

    def midpoint(self, p):
        return self.meetpoint(p, 0.5)
        
    def meetpoint(self, p, ratio):
        x = (self.x * ratio) + p.x * (1.0-ratio)
        y = (self.y * ratio) + p.y * (1.0-ratio)
        return Point(x, y)

    def pts(self):
        return [self.x, self.y]
        
    def negative(self):
        return Point(self.x, -self.y)
    
    def pointFrom(self, length, angle):
        x = self.x + length*sin(radians(angle))
        y = self.y + length*cos(radians(angle))
        return Point(x, y)
