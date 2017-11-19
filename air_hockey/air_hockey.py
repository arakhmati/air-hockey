import pygame
import numpy as np
import cv2
import os 

from air_hockey.dimensions import Dimensions
from air_hockey.circle import Puck, Mallet
from air_hockey.force import ForceRegistry, ControlledForce
from air_hockey.collision import Collision
from air_hockey.ai import AI
from air_hockey.line import Line
from air_hockey.score import Score
from air_hockey.game_info import GameInfo
from air_hockey.sprite_utils import load_sprites, blit_puck
          
class AirHockey(object):
    def __init__(self, dim=Dimensions(), video_file=None):
        
        self.dim = dim
           
        # Add Walls 
        # Arcs and Lines have to be passed in an anti-clockwise order with respect to the self.dim.center
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
        top_left_corner     = Line.generate_bezier_curve(self.dim.arc_top_left, self.dim.bezier_ratio)
        top_right_corner    = Line.generate_bezier_curve(self.dim.arc_top_right, self.dim.bezier_ratio)
        bottom_left_corner  = Line.generate_bezier_curve(self.dim.arc_bottom_left, self.dim.bezier_ratio)
        bottom_right_corner = Line.generate_bezier_curve(self.dim.arc_bottom_right, self.dim.bezier_ratio)
        
        self.borders = [top_left_wall, top_right_wall, bottom_left_wall, bottom_right_wall, left_wall, right_wall] + \
                        top_left_corner + top_right_corner + bottom_left_corner + bottom_right_corner
        
        self.puck = Puck(self.dim.center, self.dim.puck_radius, self.borders)
        
        self.top_mallet = Mallet(self.dim.top_mallet_position, self.dim.mallet_radius,
                          [top_wall, center_line, left_wall, right_wall] + top_left_corner + top_right_corner)
        
        self.bottom_mallet = Mallet(self.dim.bottom_mallet_position, self.dim.mallet_radius,
                          [center_line, bottom_wall, left_wall, right_wall] + bottom_left_corner + bottom_right_corner)
    
        self.bodies = [self.puck, self.top_mallet, self.bottom_mallet]
        
        self.top_ai    = AI(self.top_mallet,    self.puck, mode='top',    dim=self.dim)
        self.bottom_ai = AI(self.bottom_mallet, self.puck, mode='bottom', dim=self.dim)
        
        self.top_ai_force    = ControlledForce()
        self.bottom_ai_force = ControlledForce()
        
        self.forces = ForceRegistry()
        self.forces.add(self.top_mallet,    self.top_ai_force)
        self.forces.add(self.bottom_mallet, self.bottom_ai_force)
        
        self.score = Score(self.dim)
        
        # Initialize pygame variables
        pygame.init()
        self.screen = pygame.display.set_mode((self.dim.width, self.dim.height))
        self.font = pygame.font.SysFont("monospace", 30)
        pygame.display.set_caption('Air Hockey')
        
        # Initialize a video writer 
        self.writer = None
        if video_file is not None:
            if os.path.isfile(video_file): os.remove(video_file)
            self.writer = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'PIM1'), 30, 
                          (self.dim.width, self.dim.height-self.dim.vertical_margin*2))
        
        # Allocate memory for frame
        self.frame = np.zeros((self.dim.width, self.dim.height, 3), dtype=np.uint8)
        self.cropped_frame = np.zeros((self.dim.height-2*self.dim.vertical_margin, self.dim.width, 3), dtype=np.uint8)
        self.info = GameInfo(self.cropped_frame)
                
        self.reset()
    
        
    def _draw(self, puck, top_mallet, bottom_mallet, debug=False):        
        self.screen.blit(self.sprites['table'], [0,0])
        self.screen.blit(self.sprites['top_mallet'],    top_mallet - self.dim.mallet_radius)
        self.screen.blit(self.sprites['bottom_mallet'], bottom_mallet - self.dim.mallet_radius)
        
        blit_puck(self, puck)
                
        # Draw arm that controls top mallet      
        self.screen.blit(self.sprites['arm'], 
                    top_mallet - np.array((self.dim.mallet_radius, self.sprites['arm'].get_size()[1] - self.dim.mallet_radius), 
                  dtype=np.float32))

        # Draw robot that controls bottom mallet
        pygame.draw.line(self.screen, (184,184,184), 
                         [self.dim.table_left, bottom_mallet[1]], 
                         [self.dim.table_right, bottom_mallet[1]], 6) 
        
        if self.writer:
            self.writer.write(self.cropped_frame[:,:,::-1])
    
        if debug:
            for line in self.borders:
                pygame.draw.line(self.screen, (0, 255, 255), line.p2, line.p1, 6)  
     
    def _render(self, debug=False):                
        self._draw(self.puck.position, self.top_mallet.position, self.bottom_mallet.position, debug)
        self.screen.blit(self.font.render('%4d' % self.score.get_top(),    1, (200, 0, 0)), (0, 30))
        self.screen.blit(self.font.render('%4d' % self.score.get_bottom(), 1, (0, 200, 0)), (0, self.dim.rink_bottom+30))
        
        pygame.display.update()
        
        np.copyto(self.frame, pygame.surfarray.array3d(self.screen))
        np.copyto(self.cropped_frame, self.frame[:, self.dim.vertical_margin:-self.dim.vertical_margin, :].transpose((1,0,2)))
            
    def reset(self, reset_score=False):            
        if reset_score:
            self.score.reset()
            
        for body in self.bodies:
            body.reset()
            
        self.sprites = load_sprites()
        
        self._render()   
        
        return self.info
        
    def step(self, action=None, adversarial_action=None, dt=1, debug=False):
        
        if action is not None:
            if not isinstance(action, np.ndarray):
                raise Exception('Action is supposed to be a numpy array')
            elif action.shape[0] != 2:
                raise Exception('Action array can only have 2 values (x and y)')  
            elif action.min() < -1 or action.max() > 1:
                raise Exception('Values of x and y have to be in range [-1, 1]')  
            self.bottom_ai._force[:] = action

        # Compute AI moves
        if action is None:
            action = self.bottom_ai.move()
        if adversarial_action is None:
            adversarial_action = self.top_ai.move()
        
        # Update forces
        self.top_ai_force.set_force(adversarial_action)
        self.bottom_ai_force.set_force(action)
        
        # Update game info
        self.info.set_action(action)
        self.info.set_adversarial_action(adversarial_action)
        
        # Clear forces from last frame
        for body in self.bodies:
            body.clear_accumulators()
        self.forces.update_forces()
            
        # Move bodies
        for body in self.bodies:
            body.integrate(dt)
        
        # Check collisions between all possible pairs of bodies
        Collision.circle_circle([self.puck, self.top_mallet])
        Collision.circle_circle([self.top_mallet, self.bottom_mallet])
        self.info.puck_was_hit = Collision.circle_circle([self.puck, self.bottom_mallet])
        
        # Make sure all bodies are within their borders
        for body in self.bodies:
            for border in body.borders:
                Collision.circle_line(body, border)
              
        self.info.scored = self.score.update(self.puck)
        if self.info.scored is not None:
            for body in self.bodies: body.reset()
            
        self._render(debug)
        
        return self.info