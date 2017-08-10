import pygame
import numpy as np

from circle import Puck, Mallet
from force import ForceRegistry, RandomForce, KeyboardForce, ControlledForce
from collision import Collision
from ai import RuleBasedAI, MachineLearningAI
from line import Line
from score import Score
import utils
          
class World(object):
    def __init__(self):
           
        # Add Walls
        top_wall          = Line([125,  25], [375,  25])
        bottom_wall       = Line([125, 675], [375, 675])
        left_wall         = Line([ 25, 125], [ 25, 575])
        right_wall        = Line([475, 125], [475, 575])

        top_left_wall     = Line([125,  25], [200,  25])
        top_right_wall    = Line([300,  25], [375,  25])
        bottom_left_wall  = Line([125, 675], [200, 675])
        bottom_right_wall = Line([300, 675], [375, 675])
        
        center_line       = Line([ 25, 350], [475, 350])
        # Add Corners
        top_left_corner     = Line.generate_bezier_curve([[125,  25], [ 25,  25], [ 25,  125]])
        top_right_corner    = Line.generate_bezier_curve([[475, 125], [475,  25], [375,   25]])
        bottom_left_corner  = Line.generate_bezier_curve([[ 25, 575], [ 25, 675], [125,  675]])
        bottom_right_corner = Line.generate_bezier_curve([[375, 675], [475, 675], [475,  575]])
        
        self.walls = utils.flatten_list([
                      top_left_wall, top_right_wall,
                      bottom_left_wall, bottom_right_wall,
                      left_wall, right_wall,
                      top_left_corner, top_right_corner,
                      bottom_left_corner, bottom_right_corner])
        
        self.puck = Puck([250, 350], 25,
                          utils.flatten_list([
                          top_left_wall, top_right_wall,
                          bottom_left_wall, bottom_right_wall,
                          left_wall, right_wall,
                          top_left_corner, top_right_corner,
                          bottom_left_corner, bottom_right_corner]))
        
        self.top_mallet = Mallet([250, 125], 25,
                          utils.flatten_list([
                          top_wall, center_line,
                          left_wall, right_wall,
                          top_left_corner, top_right_corner]), color=(0, 0, 255))
        
        self.bottom_mallet = Mallet([250, 575], 25,
                          utils.flatten_list([
                          center_line, bottom_wall,
                          left_wall, right_wall,
                          bottom_left_corner, bottom_right_corner]))
    
        self.bodies = [self.puck, self.top_mallet, self.bottom_mallet] 
        
        self.ai = MachineLearningAI(self.top_mallet, self.puck)
        self.ai_force = ControlledForce(self.ai)
        
        self.forces = ForceRegistry()
        self.forces.add(self.bottom_mallet, KeyboardForce())
        self.forces.add(self.top_mallet, self.ai_force)
        
        self.score = Score()
                
        
    def update(self, dt, screen):
        screen.fill((255, 255, 255))
        for obj in self.bodies + self.walls:
            obj.draw(screen)
        
        # Clear forces from last frame
        for body in self.bodies:
            body.clear_accumulators()
        self.forces.update_forces(dt)
        
        # Move bodies
        for body in self.bodies:
            body.integrate(dt)
        
        # Check collisions between all possible pairs of bodies
        Collision.circle_circle(dt, [self.puck,       self.top_mallet],    restitution=0.9)
        Collision.circle_circle(dt, [self.puck,       self.bottom_mallet], restitution=0.9)
        Collision.circle_circle(dt, [self.top_mallet, self.bottom_mallet], restitution=0.1)
        
        # Make sure all bodies are within their borders
        for body in self.bodies:
            for border in body.borders:
                Collision.circle_line(body, border, screen)
                
        if self.score.update(self.puck):
            for body in self.bodies:
                body.reset()
                
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
        env.update(dt, screen)
        
        pygame.display.update()
    
    pygame.quit ()  