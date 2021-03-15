import numpy as np
import math

def vec2angle(v):
    ang = np.arctan2(*v[::-1])
    return ang % (2 * np.pi)

class Segment:
    def __init__(self, pivot, length = 100, angle = 0):
        
        self.local_angle = angle
        self.child = None

        if isinstance(pivot, list):
            self.v = np.array(pivot)
            self.parent = None
            self.global_angle = angle
        else:
            self.parent = pivot
            self.parent.child = self
            self.v = self.parent.tgt
            self.global_angle = self.parent.global_angle + angle
        
        self.length = length

        self.tgt = np.add(self.polar2xy(self.global_angle), self.v)
        self.draw()
        
    def polar2xy(self, angle):
        x = self.length * math.cos(angle)
        y = self.length * math.sin(angle)
        return [x, y] 

    def backSolve(self, tgt):
        target = np.add(tgt, - self.v)


        self.global_angle = vec2angle(target)

        if self.parent:
            self.local_angle = self.global_angle - self.parent.global_angle
        else:
            self.local_angle = self.global_angle

        self.v = np.add(self.polar2xy(self.global_angle + math.pi), tgt)

        self.tgt = np.add(self.polar2xy(self.global_angle), self.v)
        #self.update()

        if self.parent:
            self.parent.backSolve(self.v)
        else:
            # reached starting node
            self.forwardSolve(ORIGIN)
        

    def forwardSolve(self, v):
        start = np.add(v, -self.tgt)

        self.global_angle = vec2angle(start) - math.pi

        if self.parent:
            self.local_angle = self.global_angle - self.parent.global_angle
        else:
            self.local_angle = self.global_angle

        self.tgt = np.add(self.polar2xy(self.global_angle ), v)
        self.v = np.add(self.polar2xy(self.global_angle - math.pi), self.tgt)

        # print(self, self.global_angle, self.v, self.tgt)
        self.update()

        if self.child:
            self.child.forwardSolve(self.tgt)
        else:
            print("SOLVE END")