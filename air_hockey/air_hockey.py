import pygame
import itertools
import numpy as np
import cv2
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

from air_hockey.dimensions import Dimensions
from air_hockey.circle import Puck, Mallet
from air_hockey.force import ForceRegistry, RandomForce, PlayerForce, ControlledForce
from air_hockey.collision import Collision
from air_hockey.ai import AI
from air_hockey.line import Line
from air_hockey.score import Score
from air_hockey.utils import flatten_list
          
class AirHockey(object):
    def __init__(self, dim=Dimensions(), video_file=None):
        
        pygame.init()
        
        self.dim = dim
        
        self.screen = pygame.display.set_mode((self.dim.width, self.dim.height))
        pygame.display.set_caption('Air Hockey')
        
        
        self.writer = None
        if video_file is not None:
            if os.path.isfile(video_file): os.remove(video_file)
            self.writer = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'PIM1'), 30, 
                                     (self.dim.width, self.dim.height-self.dim.vertical_margin*2))
        
        
        self.frame = np.zeros((self.dim.width, self.dim.height, 3), dtype=np.uint8)
        self.cropped_frame = np.zeros((self.dim.height-2*self.dim.vertical_margin, self.dim.width, 3), dtype=np.uint8)
        
        self.state = np.zeros((128, 128, 3), dtype=np.uint8)
        self.reward = 0
           
        # Add Walls 
        # Arcs and Lines should be anti-clockwise
        # self.dim.center can be passed to Line() and Line.generate_bezier_curve() to ensure 'anti-clockwiseness'
        top_wall          = Line(self.dim.arc_top_left_start, self.dim.arc_top_right_end)
        bottom_wall       = Line(self.dim.arc_bottom_left_end, self.dim.arc_bottom_right_start)
        left_wall         = Line(self.dim.arc_top_left_end, self.dim.arc_bottom_left_start)
        right_wall        = Line(self.dim.arc_top_right_start, self.dim.arc_bottom_right_end)

        top_left_wall     = Line(self.dim.arc_top_left_start, self.dim.post_top_left)
        top_right_wall    = Line(self.dim.post_top_right, self.dim.arc_top_right_end)
        bottom_left_wall  = Line(self.dim.arc_bottom_left_end, self.dim.post_bottom_left)
        bottom_right_wall = Line(self.dim.post_bottom_right, self.dim.arc_bottom_right_start)
        
        center_line       = Line(self.dim.center_left, self.dim.center_right)
        
        # Add Corners
        top_left_corner     = Line.generate_bezier_curve(self.dim.arc_top_left,     self.dim)
        top_right_corner    = Line.generate_bezier_curve(self.dim.arc_top_right,    self.dim)
        bottom_left_corner  = Line.generate_bezier_curve(self.dim.arc_bottom_left,  self.dim)
        bottom_right_corner = Line.generate_bezier_curve(self.dim.arc_bottom_right, self.dim)
        
        self.borders = flatten_list([
                        top_left_wall, top_right_wall,
                        bottom_left_wall, bottom_right_wall,
                        left_wall, right_wall,
                        top_left_corner, top_right_corner,
                        bottom_left_corner, bottom_right_corner])
        
        self.puck = Puck(self.dim.center, self.dim.puck_radius,
                          flatten_list([
                          top_left_wall, top_right_wall,
                          bottom_left_wall, bottom_right_wall,
                          left_wall, right_wall,
                          top_left_corner, top_right_corner,
                          bottom_left_corner, bottom_right_corner]))
        
        self.top_mallet = Mallet(self.dim.top_mallet_position, self.dim.mallet_radius,
                          flatten_list([
                          top_wall, center_line,
                          left_wall, right_wall,
                          top_left_corner, top_right_corner]))
        
        self.bottom_mallet = Mallet(self.dim.bottom_mallet_position, self.dim.mallet_radius,
                          flatten_list([
                          center_line, bottom_wall,
                          left_wall, right_wall,
                          bottom_left_corner, bottom_right_corner]))
    
        self.bodies = [self.puck, self.top_mallet, self.bottom_mallet]
        self.bodies = self.bodies[::-1]
        
        self.top_ai          = AI(self.top_mallet, self.puck, mode='top', dim=self.dim)
        self.bottom_ai       = AI(self.bottom_mallet, self.puck, mode='bottom', dim=self.dim)
        
        self.top_ai_force    = ControlledForce()
        self.bottom_ai_force = ControlledForce()
        
        self.forces = ForceRegistry()
        self.forces.add(self.top_mallet,    self.top_ai_force)
        self.forces.add(self.bottom_mallet, self.bottom_ai_force)
        
        self.score = Score(self.dim)
        
        self.reset()
    
        
    
    def _draw(self, puck, top_mallet, bottom_mallet, debug=False):        
        self.screen.blit(self.table_sprite, [0,0])
        self.screen.blit(self.top_mallet_sprite,    top_mallet - self.dim.mallet_radius)
        self.screen.blit(self.bottom_mallet_sprite, bottom_mallet - self.dim.mallet_radius)
        
        # Draw the puck based on its position near the goal
        if self.dim.rink_top + self.dim.puck_radius <= puck[1] <= self.dim.rink_bottom - self.dim.puck_radius:
            self.screen.blit(self.puck_sprite, puck - self.dim.puck_radius)
        elif self.dim.rink_top - self.dim.puck_radius <= puck[1] <= self.dim.center[1]:
            if   self.dim.rink_top + self.dim.puck_radius * 0.7 <= puck[1]:
                self.screen.blit(self.puck_sprites_top[6], puck - self.dim.puck_radius)
            elif self.dim.rink_top + self.dim.puck_radius * 0.4 <= puck[1]:
                self.screen.blit(self.puck_sprites_top[5], puck - self.dim.puck_radius)
            elif self.dim.rink_top + self.dim.puck_radius * 0.1 <= puck[1]:
                self.screen.blit(self.puck_sprites_top[4], puck - self.dim.puck_radius)
            elif self.dim.rink_top - self.dim.puck_radius * 0.1 <= puck[1]:
                self.screen.blit(self.puck_sprites_top[3], puck - self.dim.puck_radius)
            elif self.dim.rink_top - self.dim.puck_radius * 0.4 <= puck[1]:
                self.screen.blit(self.puck_sprites_top[2], puck - self.dim.puck_radius)
            elif self.dim.rink_top - self.dim.puck_radius * 0.7 <= puck[1]:
                self.screen.blit(self.puck_sprites_top[1], puck - self.dim.puck_radius)
            elif self.dim.rink_top - self.dim.puck_radius       <= puck[1]:
                self.screen.blit(self.puck_sprites_top[0], puck - self.dim.puck_radius)
        elif self.dim.center[1] <= puck[1] <= self.dim.rink_bottom + self.dim.puck_radius:
            if   puck[1] <= self.dim.rink_bottom - self.dim.puck_radius * 0.7:
                self.screen.blit(self.puck_sprites_bottom[6], puck - self.dim.puck_radius)
            elif puck[1] <= self.dim.rink_bottom - self.dim.puck_radius * 0.4:
                self.screen.blit(self.puck_sprites_bottom[5], puck - self.dim.puck_radius)
            elif puck[1] <= self.dim.rink_bottom - self.dim.puck_radius * 0.1:
                self.screen.blit(self.puck_sprites_bottom[4], puck - self.dim.puck_radius)
            elif puck[1] <= self.dim.rink_bottom + self.dim.puck_radius * 0.1:
                self.screen.blit(self.puck_sprites_bottom[3], puck - self.dim.puck_radius)
            elif puck[1] <= self.dim.rink_bottom + self.dim.puck_radius * 0.4:
                self.screen.blit(self.puck_sprites_bottom[2], puck - self.dim.puck_radius)
            elif puck[1] <= self.dim.rink_bottom + self.dim.puck_radius * 0.7:
                self.screen.blit(self.puck_sprites_bottom[1], puck - self.dim.puck_radius)
            elif puck[1] <= self.dim.rink_bottom + self.dim.puck_radius:
                self.screen.blit(self.puck_sprites_bottom[0], puck - self.dim.puck_radius)
                
        # Draw the arm that controls the top mallet      
        self.screen.blit(self.top_arm_sprite, 
                    top_mallet - np.array((self.dim.mallet_radius, self.top_arm_sprite.get_size()[1] - self.dim.mallet_radius), 
                  dtype=np.float32))

        # Draw the robot that controls  the bottom mallet
        pygame.draw.line(self.screen, (0, 0, 16), 
                         [self.dim.rink_left, bottom_mallet[1]], 
                         [self.dim.rink_right, bottom_mallet[1]], 24) 
        pygame.draw.line(self.screen, (0, 0, 16), 
                         [(self.dim.table_left+self.dim.rink_left)/2, self.dim.table_bottom], 
                         [(self.dim.table_left+self.dim.rink_left)/2, self.dim.center[1]], 24) 
        pygame.draw.line(self.screen, (0, 0, 16),
                         [(self.dim.table_right+self.dim.rink_right)/2, self.dim.table_bottom], 
                         [(self.dim.table_right+self.dim.rink_right)/2, self.dim.center[1]], 24) 
        
        if self.writer:
            self.writer.write(self.cropped_frame[:,:,::-1])
    
        if debug:
            for line in self.borders:
                pygame.draw.line(self.screen, (0, 255, 255), line.p2, line.p1, 6)  
     
    def _render(self, debug=0):                
        self._draw(self.puck.position, self.top_mallet.position, self.bottom_mallet.position, debug)
        pygame.display.update()
        
        np.copyto(self.frame, pygame.surfarray.array3d(self.screen))
        np.copyto(self.cropped_frame, self.frame[:, self.dim.vertical_margin:-self.dim.vertical_margin, :].transpose((1,0,2)))
            
        
    def reset(self):
        self.score.reset()
        
        for body in self.bodies:
            body.reset()
        
#        if np.random.randint(2):
#            np.copyto(self.puck.default_position, self.dim.puck_default_position_top)
#        else:
        np.copyto(self.puck.default_position, self.dim.puck_default_position_bottom)
            
        # Diversify the data
        self.table_sprite = pygame.image.load(dir_path + '/sprites/table.png')
#        if np.random.randint(2):
#            self.table_sprite = pygame.image.load(dir_path + '/sprites/table.png')
#        else:
#            self.table_sprite = pygame.image.load(dir_path + '/sprites/flipped_table.png')
            
        self.puck_sprite          = pygame.image.load(dir_path + '/sprites/puck.png')
        self.top_mallet_sprite    = pygame.image.load(dir_path + '/sprites/top_mallet.png')
        self.bottom_mallet_sprite = pygame.image.load(dir_path + '/sprites/bottom_mallet.png')
        
        self.puck_sprites_top    = [pygame.image.load(dir_path + '/sprites/puck_top_{}.png'.format(i))    for i in range(7)]
        self.puck_sprites_bottom = [pygame.image.load(dir_path + '/sprites/puck_bottom_{}.png'.format(i)) for i in range(7)]
        
        self.top_arm_sprite = pygame.transform.flip(pygame.image.load(dir_path + '/sprites/arm_300.png'), False, True)
        self.bottom_arm_sprite = pygame.image.load(dir_path + '/sprites/arm_300.png')
        
        self._render()   
        
    def step(self, action=None, delta_time=1, n_steps=5):
        
        if action is not None:
            self.bottom_ai.force[:] = action

        # Make AI move
        self.top_ai.move()
        if action is None:
            self.bottom_ai.move()
            
        # Update forces with AI moves
        self.top_ai_force.set_force(self.top_ai.force)
        self.bottom_ai_force.set_force(self.bottom_ai.force)
        
        # Clear forces from last frame
        for body in self.bodies:
            body.clear_accumulators()
        self.forces.update_forces()
        
        self.reward =  0.0
        for i in range(n_steps):
            
            # Move bodies
            for body in self.bodies:
                body.integrate(delta_time)
            
            # Check collisions between all possible pairs of bodies
            Collision.circle_circle([self.puck, self.top_mallet])
            if Collision.circle_circle([self.puck, self.bottom_mallet]):
                self.reward = 1.0
            else:
                if self.puck.position[1] > self.dim.center[1]:
                    self.reward = -10.0
                
            Collision.circle_circle([self.top_mallet, self.bottom_mallet])
            
            # Make sure all bodies are within their borders
            for body in self.bodies:
                for border in body.borders:
                    Collision.circle_line(body, border)
                  
            scored = self.score.update(self.puck)
            if scored is not '':
                for body in self.bodies:
                    body.reset()
                print(self.score)
                if scored is 'bottom':
                    self.reward =  1000.0
                else:
                    self.reward = -10000.0
                break
            
        self._render()
        
        return self.cropped_frame, self.reward