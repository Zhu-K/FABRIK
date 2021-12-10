# Forward and Backward Reaching IK
# By Kai Zhu 2021

import numpy as np
import math

def vec2angle(v):
    ang = np.arctan2(*v[::-1])
    return ang % (2 * np.pi)

class Segment:
# Segment class to represent one segment in an IK chain, with starting pos at v, and end pos at tgt.
# Also tracks global and local rotations, the local angle being analogous to a servo angle

    def __init__(self, pivot, length = 100, angle = 0):
        
        self.local_angle = angle

        if isinstance(pivot, list):
            self.v = np.array(pivot)
            self.parent = None
            self.global_angle = angle
        else:
            self.parent = pivot
            self.v = self.parent.tgt
            self.global_angle = self.parent.global_angle + angle
        
        self.length = length

        self.tgt = np.add(self.polar2xy(self.global_angle), self.v)
        
    def polar2xy(self, angle):
        # converts rotation angle to an end point xy on the cartesian plane using segment length

        x = self.length * math.cos(angle)
        y = self.length * math.sin(angle)
        return [x, y] 

class IKChain:
# IK class as a set of segments and methods to render and solve the IK of the segments

    def __init__(self, origin: list, lengths: list):
        self.canvas = None
        self.origin = origin
        self.segments = [Segment(origin, lengths[0], 0)]
        for length in lengths[1:]:
            self.segments.append(Segment(self.segments[-1], length, 0))

    def draw(self, canvas):
        # initial drawing of the IK system on input canvas

        self.canvas = canvas
        for seg in self.segments:
            seg.line = canvas.create_line(seg.v[0], seg.v[1], seg.tgt[0], seg.tgt[1], fill="gray", width = 5, tag = ("segment"))
            seg.joint = canvas.create_oval(seg.v[0] - 5, seg.v[1] - 5, seg.v[0] + 5, seg.v[1] + 5, fill="yellow", outline="yellow", tag = "joint")  # resetting start
    
    def update(self):
        # update renderings of IK system

        for seg in self.segments:
            self.canvas.coords(seg.joint, seg.v[0] - 5, seg.v[1] - 5, seg.v[0] + 5, seg.v[1] + 5)
            self.canvas.coords(seg.line, seg.v[0], seg.v[1], seg.tgt[0], seg.tgt[1])

    def solve(self, tgt, fixed=True):
        # reverse IK (moves segments toward the target)

        for seg in self.segments[::-1]:
            target = np.add(tgt, - seg.v)

            seg.global_angle = vec2angle(target)

            if seg.parent:
                seg.local_angle = seg.global_angle - seg.parent.global_angle
                # if seg.local_angle < 0.2:               # angle limit test
                #     seg.global_angle = 0.2 + seg.parent.global_angle

            else:
                seg.local_angle = seg.global_angle
                # if seg.local_angle < 0.5:               # angle limit test
                #     seg.global_angle = 0.5

            seg.v = np.add(seg.polar2xy(seg.global_angle + math.pi), tgt)

            seg.tgt = np.add(seg.polar2xy(seg.global_angle), seg.v)

            tgt = seg.v

        # do forward IK only if origin is fixed
        if not fixed:
            return

        # forward IK (moves segments toward origin)
        v = self.origin
        for seg in self.segments:
            start = np.add(v, - seg.tgt)

            seg.global_angle = vec2angle(start) - math.pi

            if seg.parent:
                seg.local_angle = seg.global_angle - seg.parent.global_angle
            else:
                seg.local_angle = seg.global_angle

            seg.tgt = np.add(seg.polar2xy(seg.global_angle ), v)
            seg.v = np.add(seg.polar2xy(seg.global_angle - math.pi), seg.tgt)

            # print(self, self.global_angle, self.v, self.tgt)
            v = seg.tgt
    
    def clearCanvas(self):
        # call this method to remove the drawn segments from canvas

        if self.canvas:
            for seg in self.segments:
                self.canvas.delete(seg.line)
                self.canvas.delete(seg.joint)   