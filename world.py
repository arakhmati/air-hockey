import pygame
import numpy as np

from circle import Puck, Mallet
from force import ForceRegistry, RandomForce, KeyboardForce, ControlledForce
from collision import Collision
from ai import RuleBasedAI, MachineLearningAI
from line import Line
from score import Score
import utils
import dimensions as D
import colors as C
import physical_constants as P

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
          
class World(object):
    def __init__(self):
           
        # Add Walls (Anti-clockwise Arcs)
        top_wall          = Line(D.arc_top_left_start, D.arc_top_right_end)
        bottom_wall       = Line(D.arc_bottom_left_end, D.arc_bottom_right_start)
        left_wall         = Line(D.arc_top_left_end, D.arc_bottom_left_start)
        right_wall        = Line(D.arc_top_right_start, D.arc_bottom_right_end)

        top_left_wall     = Line(D.arc_top_left_start, D.post_top_left)
        top_right_wall    = Line(D.post_top_right, D.arc_top_right_end)
        bottom_left_wall  = Line(D.arc_bottom_left_end, D.post_bottom_left)
        bottom_right_wall = Line(D.post_bottom_right, D.arc_bottom_right_start)
        
        center_line       = Line(D.center_left, D.center_right)
        
        # Add Corners
        top_left_corner, self.top_left_corner_points = Line.generate_bezier_curve([D.arc_top_left_start, 
                                                                                   D.arc_top_left_center, D.arc_top_left_end])
        top_right_corner, self.top_right_corner_points = Line.generate_bezier_curve([D.arc_top_right_start, 
                                                                                   D.arc_top_right_center, D.arc_top_right_end])
        bottom_left_corner, self.bottom_left_corner_points = Line.generate_bezier_curve([D.arc_bottom_left_start, 
                                                                                   D.arc_bottom_left_center, D.arc_bottom_left_end])
        bottom_right_corner, self.bottom_right_corner_points = Line.generate_bezier_curve([D.arc_bottom_right_start,
                                                                                   D.arc_bottom_right_center, D.arc_bottom_right_end])
        
        self.puck = Puck(D.center, D.body_radius,
                          utils.flatten_list([
                          top_left_wall, top_right_wall,
                          bottom_left_wall, bottom_right_wall,
                          left_wall, right_wall,
                          top_left_corner, top_right_corner,
                          bottom_left_corner, bottom_right_corner]), C.puck)
        
        self.top_mallet = Mallet(D.top_mallet_position, D.body_radius,
                          utils.flatten_list([
                          top_wall, center_line,
                          left_wall, right_wall,
                          top_left_corner, top_right_corner]), C.top_mallet)
        
        self.bottom_mallet = Mallet(D.bottom_mallet_position, D.body_radius,
                          utils.flatten_list([
                          center_line, bottom_wall,
                          left_wall, right_wall,
                          bottom_left_corner, bottom_right_corner]), C.bottom_mallet)
    
        self.bodies = [self.puck, self.top_mallet, self.bottom_mallet] 
        
        self.ai = MachineLearningAI(self.top_mallet, self.puck)
        self.ai_force = ControlledForce(self.ai)
        
        self.forces = ForceRegistry()
        self.forces.add(self.bottom_mallet, KeyboardForce())
        self.forces.add(self.top_mallet, self.ai_force)
        
        self.score = Score()
        
        self.circles = [D.circle_top_left, D.circle_top_right, D.circle_bottom_left, D.circle_bottom_right]
        
        def compute_arc(arc_points, center_point):
            arc_points = [[int(x), int(y)] for (x, y) in [v.get_xy() for v in arc_points]]
            arc_points.sort(key=lambda x: x[1])
#            print(arc_points)
            x, y = center_point
            if x < D.center[0]: center_point[0] -= 5
            else:               center_point[0] += 5
            if y < D.center[1]:
                extra_point = [center_point[0], arc_points[-1][1]]
                output = arc_points + [extra_point, center_point]
            else:
                extra_point = [center_point[0], arc_points[0][1]]
                output = arc_points + [center_point, extra_point]
            
            return output
        self.arcs = [compute_arc(self.top_left_corner_points, D.arc_top_left_center)]
        self.arcs.append(compute_arc(self.top_right_corner_points, D.arc_top_right_center))
        self.arcs.append(compute_arc(self.bottom_left_corner_points, D.arc_bottom_left_center))
        self.arcs.append(compute_arc(self.bottom_right_corner_points, D.arc_bottom_right_center))
        self.walls = utils.flatten_list([
                      top_left_wall, top_right_wall,
                      bottom_left_wall, bottom_right_wall])
    
        self.bg = Background('/home/ahmed/Downloads/table.jpg', [0,0])
        self.puck_s = Background('/home/ahmed/Downloads/puck.png', self.puck.position.get_xy())
        self.tm_s = Background('/home/ahmed/Downloads/mallet.png', self.top_mallet.position.get_xy())
        self.bm_s = Background('/home/ahmed/Downloads/mallet.png', self.bottom_mallet.position.get_xy())
                
        
    def step(self, dt):
        
        # Clear forces from last frame
        for body in self.bodies:
            body.clear_accumulators()
        self.forces.update_forces(dt)
        
        # Move bodies
        for body in self.bodies:
            body.integrate(dt)
        
        # Check collisions between all possible pairs of bodies
        Collision.circle_circle(dt, [self.puck,       self.top_mallet],    restitution=P.puck_mallet_restitution)
        Collision.circle_circle(dt, [self.puck,       self.bottom_mallet], restitution=P.puck_mallet_restitution)
        Collision.circle_circle(dt, [self.top_mallet, self.bottom_mallet], restitution=P.mallet_mallet_restitution)
        
        # Make sure all bodies are within their borders
        for body in self.bodies:
            for border in body.borders:
                Collision.circle_line(body, border)
                
        if self.score.update(self.puck):
            for body in self.bodies:
                body.reset()
                
    def draw(self, screen):
        
        screen.blit(self.bg.image, self.bg.rect)
        screen.blit(self.puck_s.image, np.array(self.puck.position.get_xy())-np.array([self.puck.radius, self.puck.radius]))
        screen.blit(self.tm_s.image, np.array(self.top_mallet.position.get_xy())-np.array([self.puck.radius, self.puck.radius]))
        screen.blit(self.bm_s.image, np.array(self.bottom_mallet.position.get_xy())-np.array([self.puck.radius, self.puck.radius]))

#        screen.fill(C.table)
#        pygame.draw.rect(screen, C.rink, [D.rink_left, D.rink_top, D.rink_width, D.rink_height])
#        for arc in self.arcs:
#            pygame.draw.polygon(screen, (0, 0, 0), arc)
#        for line in self.walls:
#            pygame.draw.line(screen, (0, 0, 0), line.p2.get_xy(), line.p1.get_xy(), 6)
#            
#        
#        pygame.draw.circle(screen, C.rink_lines, D.center, 6)
#        pygame.draw.line(screen, C.rink_lines, D.center_left, D.post_center_left,   6)
#        pygame.draw.line(screen, C.rink_lines, D.post_center_right, D.center_right, 6)
#        for obj in self.circles:
#            pygame.draw.circle(screen, C.rink_lines, obj, D.rink_circle_radius, 2)            
#            
#        for obj in self.bodies:
#            pygame.draw.circle(screen, obj.color, np.array(obj.position.get_xy()).astype(int), obj.radius)
            
            
        
                
if __name__ == "__main__":
    pygame.init()
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((D.width, D.height))
    
    env = World()

    done = False
    while not done:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
        dt = clock.tick_busy_loop(90)
        env.step(dt)
        env.draw(screen)
        
        pygame.display.update()
    
    pygame.quit ()  