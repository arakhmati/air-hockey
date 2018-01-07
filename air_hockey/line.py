import numpy as np
import air_hockey.vector as V

class Line(object):

    def __init__(self, p1, p2):
        self.p1 = np.copy(p1)
        self.p2 = np.copy(p2)

        self.direction = V.normalize(self.p2 - self.p1)
        self.normal = np.array([self.direction[1], -self.direction[0]])

    @staticmethod
    def generate_bezier_curve(arc_points, bezier_ratio):
        if len(arc_points) != 3:
            raise ValueError('Bezier curve can be generated only using 3 points')

        arc_points = [np.array(point, dtype=np.float32) for point in arc_points]
        p0, p1, p2 = arc_points

        points = []
        # Generate Bezier
        for ratio in np.arange(0.0, 1.0, bezier_ratio):
            distance = (p1 - p0)
            np0 = p0 + distance * ratio
            distance = (p2 - p1)
            np1 = p1 + distance * ratio
            points.append(np0 + (np1 - np0) * ratio)
        points.append(p2)

        lines = []
        for i in range(len(points)-1):
            lines.append(Line(points[i], points[i+1]))

        return lines

    def __repr__(self):
        return str(self.p1) + ' ' + str(self.p2)
