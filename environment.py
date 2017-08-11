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

# http://resizeimage.net/
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image_file):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
          
class Environment(object):
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
        self.borders = utils.flatten_list([
                        top_left_wall, top_right_wall,
                        bottom_left_wall, bottom_right_wall,
                        left_wall, right_wall,
                        top_left_corner, top_right_corner,
                        bottom_left_corner, bottom_right_corner])
        
        self.puck = Puck(D.center, D.puck_radius,
                          utils.flatten_list([
                          top_left_wall, top_right_wall,
                          bottom_left_wall, bottom_right_wall,
                          left_wall, right_wall,
                          top_left_corner, top_right_corner,
                          bottom_left_corner, bottom_right_corner]), C.puck)
        
        self.top_mallet = Mallet(D.top_mallet_position, D.mallet_radius,
                          utils.flatten_list([
                          top_wall, center_line,
                          left_wall, right_wall,
                          top_left_corner, top_right_corner]), C.top_mallet)
        
        self.bottom_mallet = Mallet(D.bottom_mallet_position, D.mallet_radius,
                          utils.flatten_list([
                          center_line, bottom_wall,
                          left_wall, right_wall,
                          bottom_left_corner, bottom_right_corner]), C.bottom_mallet)
    
        self.bodies = [self.puck, self.top_mallet, self.bottom_mallet] 
        
        self.top_ai = MachineLearningAI(self.top_mallet, self.puck, mode='top')
        self.top_ai_force = ControlledForce(self.top_ai)
        self.bottom_ai = MachineLearningAI(self.bottom_mallet, self.puck, mode='bottom')
        self.bottom_ai_force = ControlledForce(self.bottom_ai)
        
        self.forces = ForceRegistry()
        self.forces.add(self.top_mallet, self.top_ai_force)
        self.forces.add(self.bottom_mallet, self.bottom_ai_force)
        
        self.score = Score()
    
        self.table_sprite         = Sprite('sprites/table.png')
        self.puck_sprite          = Sprite('sprites/puck.png')
        self.top_mallet_sprite    = Sprite('sprites/top_mallet.png')
        self.bottom_mallet_sprite = Sprite('sprites/bottom_mallet.png')
        
    def step(self, dt):
        
        # Make AI move
        self.top_ai.move()
        self.bottom_ai.move()
        
        # Clear forces from last frame
        for body in self.bodies:
            body.clear_accumulators()
        self.forces.update_forces(dt)
        
        # Move bodies
        for body in self.bodies:
            body.integrate(dt)
            
#        # Make sure all bodies are within their borders
#        for body in self.bodies:
#            for border in body.borders:
#                Collision.circle_line(body, border)
        
        # Check collisions between all possible pairs of bodies
        for i in range(3): # Loop to prevent the objects from going each other when the bounce
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
            print(self.score)
            
        return self.bottom_ai.force
                
    def draw(self, screen):
        
        screen.blit(self.table_sprite.image, [0,0])
        screen.blit(self.puck_sprite.image, self.puck.position-np.array([self.puck.radius, self.puck.radius]))
        screen.blit(self.top_mallet_sprite.image, self.top_mallet.position-np.array([self.puck.radius, self.puck.radius]))
        screen.blit(self.bottom_mallet_sprite.image, self.bottom_mallet.position-np.array([self.puck.radius, self.puck.radius]))
        
        for line in self.borders:
            pygame.draw.line(screen, (255, 0, 0), line.p2, line.p1, 6)        