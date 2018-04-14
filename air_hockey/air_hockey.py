import pygame
import numpy as np
import cv2
import os

from air_hockey.dimensions import Dimensions
from air_hockey.circle import Puck, Mallet, Target
from air_hockey.force import ForceRegistry, ControlledForce
from air_hockey.collision import Collision
from air_hockey.ai import AI
from air_hockey.line import Line
from air_hockey.score import Score
from air_hockey.game_info import GameInfo
from air_hockey.sprite_utils import load_sprites, blit_puck
import air_hockey.vector as V
import air_hockey.phy_const as P


default_use_object={'arm': True,
                    'puck': True,
                    'top_mallet': True}

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
        
        self.bottom_target = Target([self.dim.center[0], self.dim.rink_bottom - 55], self.dim.target_radius)

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
        
        self.distance = P.max_distance

        self.reset()


    def _draw(self, puck, top_mallet, bottom_mallet, debug=False, use_object=default_use_object):
        
        draw_arm = use_object['arm']
        draw_puck = use_object['puck']
        draw_top_mallet = use_object['top_mallet']
        
        self.screen.blit(self.sprites['table'], [0,0])
        
        # Draw dark blue target to which the robot mallet should when the puck is on the opposite side
        pygame.draw.circle(self.screen, (0,0,139), self.bottom_target.position, self.bottom_target.radius)
        
        if draw_top_mallet:
            self.screen.blit(self.sprites['top_mallet'],    top_mallet - self.dim.mallet_radius)
        
        self.screen.blit(self.sprites['bottom_mallet'], bottom_mallet - self.dim.mallet_radius)

        if draw_puck:
            blit_puck(self, puck)

        if draw_arm:
            # Draw arm that controls top mallet
            y_offset = self.sprites['arm'].get_size()[1] - self.dim.mallet_radius
            if self.dominant_arm == 'right':
                x_offset = self.dim.mallet_radius
            else:
                x_offset = self.sprites['arm'].get_size()[0] - self.dim.mallet_radius
            self.screen.blit(self.sprites['arm'], top_mallet - np.array((x_offset, y_offset), dtype=np.float32))

        # Draw robot that controls bottom mallet
        pygame.draw.line(self.screen, (184,184,184),
                         [self.dim.table_left, bottom_mallet[1]],
                         [self.dim.table_right, bottom_mallet[1]], 6)
        
        

        if self.writer:
            self.writer.write(self.cropped_frame[:,:,::-1])

        if debug:
            for line in self.borders:
                pygame.draw.line(self.screen, (0, 255, 255), line.p2, line.p1, 6)

    def _render(self, debug=False, use_object=default_use_object):
        self._draw(self.puck.position, self.top_mallet.position, self.bottom_mallet.position, debug, use_object)
        self.screen.blit(self.font.render('%4d' % self.score.get_top(),    1, (200, 0, 0)), (0, 30))
        self.screen.blit(self.font.render('%4d' % self.score.get_bottom(), 1, (0, 200, 0)), (0, self.dim.rink_bottom+30))

        pygame.display.update()

        self.frame[:] = pygame.surfarray.array3d(self.screen)
        self.cropped_frame[:] = self.frame[:, self.dim.vertical_margin:-self.dim.vertical_margin, :].transpose((1,0,2))

    def reset(self,
              scored=False,
              puck_was_hit=False,
              puck_is_at_the_bottom=False,
              distance_decreased=False,
              hit_the_border=False,
              use_object=default_use_object):

        self.puck.reset(self.dim, self.dim.rink_top, self.dim.rink_bottom)
        self.top_mallet.reset(self.dim, self.dim.rink_top, self.dim.center[1])
        self.bottom_mallet.reset(self.dim, self.dim.center[1], self.dim.rink_bottom)

        # Resolve possible interpenetration
        Collision.circle_circle([self.puck, self.top_mallet])
        Collision.circle_circle([self.top_mallet, self.bottom_mallet])
        
        in_the_target = Collision.circle_circle([self.bottom_mallet, self.bottom_target], resolve=False)

        self.sprites, self.dominant_arm = load_sprites()

        self._render(use_object=use_object)

        return GameInfo(self.cropped_frame,
                        scored=scored,
                        puck_was_hit=puck_was_hit,
                        puck_is_at_the_bottom=puck_is_at_the_bottom,
                        distance_decreased=distance_decreased,
                        hit_the_border=hit_the_border,
                        in_the_target=in_the_target)

    def step(self,
             robot_action=None,
             human_action=None,
             debug=False,
             use_object=default_use_object,
             n_steps=4):

        dt = np.random.ranf() + 1 # dt is randomly in interval [1, 2)

        if robot_action is not None:
            if not isinstance(robot_action, np.ndarray):
                raise Exception('Action is supposed to be a numpy array')
            elif robot_action.shape[0] != 2:
                raise Exception('Action array can only have 2 values (x and y)')
            elif robot_action.min() < -1 or robot_action.max() > 1:
                raise Exception('Values of x and y have to be in range [-1, 1]')

        if human_action is not None:
            if not isinstance(human_action, np.ndarray):
                raise Exception('Adversarial action is supposed to be a numpy array')
            elif human_action.shape[0] != 2:
                raise Exception('Adversarial action array can only have 2 values (x and y)')
            elif human_action.min() < -1 or human_action.max() > 1:
                raise Exception('Adversarial values of x and y have to be in range [-1, 1]')

        # Compute AI moves
        if robot_action is None:
            if use_object['puck']:
                robot_action = self.bottom_ai.move()
            else:
                robot_action = [0, 0]
        if human_action is None:
            if use_object['arm'] and use_object['top_mallet']:
                human_action = self.top_ai.move()
            elif not use_object['puck']:
                human_action = [0, 0]
            else:
                human_action = [0, 0]
                

        # Update forces
        self.top_ai_force.set_force(human_action)
        self.bottom_ai_force.set_force(robot_action)
        
        for _ in range(n_steps):

            # Clear forces from last frame
            for body in self.bodies:
                body.clear_accumulators()
            self.forces.update_forces()
    
            # Move bodies
            for body in self.bodies:
                body.integrate(dt)
    
            # Check collisions between all possible pairs of bodies
            
            if use_object['arm'] or use_object['top_mallet']:
                Collision.circle_circle([self.puck, self.top_mallet])
            Collision.circle_circle([self.top_mallet, self.bottom_mallet])
            
            if use_object['puck']:
                puck_was_hit = Collision.circle_circle([self.puck, self.bottom_mallet])
            else:
                puck_was_hit = False
            
            in_the_target = Collision.circle_circle([self.bottom_mallet, self.bottom_target], resolve=False)
    
            # Make sure all bodies are within their borders
            collided = [False, False, False]
            for i, body in enumerate(self.bodies):
                for border in body.borders:
                    if (Collision.circle_line(body, border)):
                        collided[i] = True
            hit_the_border = collided[2]
    
            puck_is_at_the_bottom = self.puck.position[1] > self.dim.center[1]
    
            distance_decreased = False
            if puck_is_at_the_bottom:
                distance = V.magnitude(self.puck.position - self.bottom_mallet.position)
                distance_decreased = distance < self.distance
                self.distance = distance
            else:
                self.distance = P.max_distance
    
            scored = self.score.update(self.puck)
            if scored is not None:
                return self.reset(scored,
                                  puck_was_hit,
                                  puck_is_at_the_bottom,
                                  distance_decreased,
                                  hit_the_border)
    
            self._render(debug, use_object)

        return GameInfo(self.cropped_frame,
                        robot_action,
                        human_action,
                        scored,
                        puck_was_hit,
                        puck_is_at_the_bottom,
                        distance_decreased,
                        hit_the_border,
                        in_the_target)
        