import pygame
import numpy as np

from vector import Vector
from circle import Puck, Mallet
from force import ForceRegistry, RandomForce, KeyboardForce, InputForce
from contact import Contact
from ai import RuleBasedAI, MachineLearningAI
from line import Line
          
class World(object):
    def __init__(self):
        

######### Add Static Objects ########################################################################
        # Points must be right to left or top to bottom        

        # Add Walls
        self.top_left_wall     = Line([125,  25], [200,  25])
        self.top_right_wall    = Line([300,  25], [375,  25])
        self.bottom_left_wall  = Line([125, 675], [200, 675])
        self.bottom_right_wall = Line([300, 675], [375, 675])
        self.left_wall         = Line([ 25, 125], [ 25, 575])
        self.right_wall        = Line([475, 125], [475, 575])
        # Add Corners
        self.top_left_corner     = Line.generate_bezier_curve([[125,  25], [ 25,  25], [ 25,  125]])
        self.top_right_corner    = Line.generate_bezier_curve([[475, 125], [475,  25], [375,   25]])
        self.bottom_left_corner  = Line.generate_bezier_curve([[ 25, 575], [ 25, 675], [125,  675]])
        self.bottom_right_corner = Line.generate_bezier_curve([[375, 675], [475, 675], [475,  575]])
        
        self.walls = [self.top_left_wall, self.top_right_wall,
                      self.bottom_left_wall, self.bottom_right_wall,
                      self.left_wall, self.right_wall,
                      self.top_left_corner, self.top_right_corner,
                      self.bottom_left_corner, self.bottom_right_corner]
        import collections
        def flatten(x):
            if isinstance(x, collections.Iterable):
                return [a for i in x for a in flatten(i)]
            else:
                return [x]
        self.walls = flatten(self.walls)
        
######### Add Dynamic Objects #######################################################################
        puck          = Puck([250, 350], 25)
        top_mallet    = Mallet([250, 125], 25)
        bottom_mallet = Mallet([175, 575], 25)
        
        
#        self.ai = MachineLearningAI(self.bodies[2], self.bodies[0])
        
        
#        self.aiforce = InputForce()
        self.forces = ForceRegistry()
#        self.forces.add(bottom_mallet, self.aiforce)
        self.forces.add(bottom_mallet, KeyboardForce())
        self.forces.add(top_mallet, RandomForce())
                
        self.bodies = [puck, top_mallet, bottom_mallet]

    @staticmethod
    def circle_line_collision(body, line):
        seg_a = line.p1
        seg_b = line.p2
        circ_pos = body.position
        
        seg_v = seg_b - seg_a        
        pt_v = circ_pos - seg_a
        
        proj_mag = pt_v * seg_v.normalize()
        
#        print(proj_mag)
        
#        if proj_mag <= 0:
#            closest = seg_a
#        elif proj_mag >= seg_v.magnitude():
#            closest = seg_b
#        else:
        proj_v = seg_v.normalize() * proj_mag
        closest = seg_a + proj_v
        
        x, y = closest.get_xy()
        x1, y1 = seg_a.get_xy()
        x2, y2 = seg_b.get_xy()
        
        if x1 - x2 > 0:
            x = min(x, x1)
            x = max(x, x2)
        else:
            x = max(x, x1)
            x = min(x, x2)
        
        if y1 - y2 > 0:
            y = min(y, y1)
            y = max(y, y2)
        else:
            y = max(y, y1)
            y = min(y, y2)
            
        closest = Vector([x, y])
        
            
        x, y = closest.get_xy()
        pygame.draw.circle(screen, (0, 255, 0), [int(x), int(y)],  6, 0)
            
        dist_v = circ_pos - closest
        if dist_v.magnitude() < body.radius:
        
        
#        ac = line.p1 - body.position
#        ab = line.p1 - line.p2
##        print(ac.cross(ab) / ab.magnitude())
#        if (ac.cross(ab) / ab.magnitude()) < body.radius:
#            print(line)
            
            # Resovle interpenetration
            direction = (line.p2 - line.p1).normalize()
            toCenter = body.position - line.p1
            perpComponent = toCenter - direction * (toCenter *  direction)
            penetrationDepth = body.radius - perpComponent.magnitude()
            mvmtToCorrectPosition = perpComponent.normalize() * penetrationDepth
            body.position += mvmtToCorrectPosition
            
            # Resolve Velocity
            body.velocity -= line.normal * (body.velocity * line.normal) * 2 * body.wall_restitution
    
    @staticmethod
    def circle_circle_collision(bodies, dt, restitution=0.9):
        position_0 = bodies[0].position
        position_1 = bodies[1].position
        total_radius = bodies[0].radius + bodies[1].radius
        
        middle = position_0 - position_1
        distance = middle.magnitude()
        
        if distance <= 0.0 or distance >= (total_radius):
            return None
        
        normal = middle * (1.0/distance)
        penetration = total_radius - distance
        
        Contact(bodies, normal, penetration, restitution).resolve(dt)
            
    def update(self, dt, screen):
        for body in self.bodies:
            body.draw(screen)
        
        for body in self.bodies:
            body.clear_accumulators()
            
#        self.aiforce.set_force(self.ai.move())
            
        self.forces.update_forces(dt)
        
        # Move body based 
        for body in self.bodies:
            body.integrate(dt)
            for line in self.walls:
                self.circle_line_collision(body, line)
        
        for line in self.walls:
            pygame.draw.line(screen, (0, 0, 0), line.p1.get_xy(), line.p2.get_xy(), 5)
            
            
        for i in range(len(self.bodies)):
            for j in range(i, len(self.bodies)):
                if i == j: continue
                self.circle_circle_collision((self.bodies[i], self.bodies[j]), dt)
                
                    
    
if __name__ == "__main__":

    pygame.init()
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((500, 700))
    
    env = World()

    done = False
    while not done:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
        dt = clock.tick_busy_loop(60)
        
        screen.fill((255, 255, 255))
#        pygame.draw.rect(screen, (255, 255, 255), (25, 25, 450, 650), 0)
        env.update(dt, screen)
        
        pygame.display.update()
#        done = True
    
    
    pygame.quit ()  