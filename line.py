import pygame
import numpy as np

from vector import Vector

class Line(object):
    
    @staticmethod
    def _edge_sum(p1, p2):
        x1, y1 = p1.get_xy()
        x2, y2 = p2.get_xy()
        return (x2 - x1) * (y2 + y1)
    
    def __init__(self, p1, p2):
        self.p1, self.p2 = [Vector(point) if not isinstance(point, Vector) else point for point in [p1, p2]]     
#        print(type(self.p1))

        # TODO: make parametric
        sum_over_edges  = Line._edge_sum(self.p1, Vector([250, 350]))
        sum_over_edges += Line._edge_sum(Vector([250, 350]), self.p2)
        sum_over_edges += Line._edge_sum(self.p2, self.p1)
        if sum_over_edges > 0: # Points are clockwise
            self.p1, self.p2 = self.p2, self.p1 # Swap end points to make them counter-clockwise

        dx, dy = (self.p2 - self.p1).normalize().get_xy()
        self.normal = Vector([dy, -dx])
        self.direction = (self.p2 - self.p1).normalize()
#        print(self.normal)
        
    @staticmethod
    def generate_bezier_curve(arc_points, ratio=0.1):
        if len(arc_points) != 3:
            raise ValueError('Bezier curve can be generated only using 3 points')
            
        arc_points = [Vector(point) for point in arc_points]
        p0, p1, p2 = arc_points
            
        # Make sure points are counter-clockwise
        sum_over_edges  = Line._edge_sum(p0, p1)
        sum_over_edges += Line._edge_sum(p1, p2)
        sum_over_edges += Line._edge_sum(p2, p0)
        if sum_over_edges < 0: # Points are clockwise
            p0, p2 = p2, p0 # Swap end points to make them counter-clockwise
            
        points = []
        # Generate Bezier
        for r in np.arange(0.0, 1.0, ratio):
            distance = (p1 - p0)
            np0 = p0 + distance * r
            distance = (p2 - p1)
            np1 = p1 + distance * r
            points.append(np0 + (np1 - np0) * r)
        points.append(p2)
        
        lines = []
        for i in range(len(points)-1):
            lines.append(Line(points[i], points[i+1]))          
        
        return lines
    
    def draw(self, screen):
        pygame.draw.line(screen, (0, 0, 0), self.p1.get_xy(), self.p2.get_xy(), 5)
    
    def __repr__(self):
        return str(self.p1) + ' ' + str(self.p2)
        