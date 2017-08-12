import itertools
import numpy as np

from circle import Puck, Mallet
from force import ForceRegistry, RandomForce, PlayerForce, ControlledForce
from collision import Collision
from ai import RuleBasedAI, MachineLearningAI
from line import Line
from score import Score
import utils
import dimensions as D
import colors as C
import physical_constants as P
          
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
        top_left_corner = Line.generate_bezier_curve([D.arc_top_left_start, D.arc_top_left_center, D.arc_top_left_end])
        top_right_corner = Line.generate_bezier_curve([D.arc_top_right_start, D.arc_top_right_center, D.arc_top_right_end])
        bottom_left_corner = Line.generate_bezier_curve([D.arc_bottom_left_start, D.arc_bottom_left_center, D.arc_bottom_left_end])
        bottom_right_corner = Line.generate_bezier_curve([D.arc_bottom_right_start, D.arc_bottom_right_center, D.arc_bottom_right_end])
        
        self.borders = utils.flatten_list([
                        top_left_wall, top_right_wall,
                        bottom_left_wall, bottom_right_wall,
                        left_wall, right_wall,
                        top_left_corner, top_right_corner,
                        bottom_left_corner, bottom_right_corner])
        
        self.puck = Puck('p', D.center, D.puck_radius,
                          utils.flatten_list([
                          top_left_wall, top_right_wall,
                          bottom_left_wall, bottom_right_wall,
                          left_wall, right_wall,
                          top_left_corner, top_right_corner,
                          bottom_left_corner, bottom_right_corner]))
        
        self.top_mallet = Mallet('tm', D.top_mallet_position, D.mallet_radius,
                          utils.flatten_list([
                          top_wall, center_line,
                          left_wall, right_wall,
                          top_left_corner, top_right_corner]))
        
        self.bottom_mallet = Mallet('bm', D.bottom_mallet_position, D.mallet_radius,
                          utils.flatten_list([
                          center_line, bottom_wall,
                          left_wall, right_wall,
                          bottom_left_corner, bottom_right_corner]))
    
        self.bodies = [self.puck, self.top_mallet, self.bottom_mallet]
        self.bodies = self.bodies[::-1]
        
        self.top_ai          = MachineLearningAI(self.top_mallet, self.puck, mode='top')
        self.top_ai_force    = ControlledForce(self.top_ai)
        self.bottom_ai       = MachineLearningAI(self.bottom_mallet, self.puck, mode='bottom')
        self.bottom_ai_force = ControlledForce(self.bottom_ai)
        
        self.forces = ForceRegistry()
        self.forces.add(self.top_mallet,    self.top_ai_force)
        self.forces.add(self.bottom_mallet, self.bottom_ai_force)
#        self.forces.add(self.bottom_mallet, PlayerForce(player=0))
        
        self.score = Score()
        
        self.observations = np.zeros((4, 2), dtype=np.float32)
    
        import pygame
        self.table_sprite         = pygame.image.load('sprites/table.png')
        self.puck_sprite          = pygame.image.load('sprites/puck.png')
        self.top_mallet_sprite    = pygame.image.load('sprites/top_mallet.png')
        self.bottom_mallet_sprite = pygame.image.load('sprites/bottom_mallet.png')
        
        self.puck_sprites_top    = [pygame.image.load('sprites/puck_top_{}.png'.format(i))    for i in range(7)]
        self.puck_sprites_bottom = [pygame.image.load('sprites/puck_bottom_{}.png'.format(i)) for i in range(7)]
        
        self.top_arm_sprite = pygame.transform.flip(pygame.image.load('sprites/arm_300.png'), False, True)
        self.bottom_arm_sprite = pygame.image.load('sprites/arm_300.png')
        
    def step(self, delta_time=1, actions=None):
        
        # Make AI move
        self.top_ai.move()
        self.bottom_ai.move()
        
        # Clear forces from last frame
        for body in self.bodies:
            body.clear_accumulators()
        self.forces.update_forces()
        
        # Move bodies
        for body in self.bodies:
            body.integrate(delta_time)
        
        # Check collisions between all possible pairs of bodies
        for pair in itertools.combinations(self.bodies, r=2):
            Collision.circle_circle(pair)
        
        # Make sure all bodies are within their borders
        self.points = {'p': [], 'tm': [], 'bm': []}
        for body in self.bodies:
            for border in body.borders:
                self.points[body.name].append(Collision.circle_line(body, border))
                
        if self.score.update(self.puck):
            for body in self.bodies:
                body.reset()
            print(self.score)
            
        self.observations[0] = self.puck.position
        self.observations[1] = self.top_mallet.position
        self.observations[2] = self.bottom_mallet.position
#        self.observations[3] = self.puck.position
            
        return self.observations
    
    def draw(self, screen, puck, top_mallet, bottom_mallet, debug=False):
        import pygame
        
        screen.blit(self.table_sprite, [0,0])
        screen.blit(self.top_mallet_sprite,    top_mallet - D.mallet_radius)
        screen.blit(self.bottom_mallet_sprite, bottom_mallet - D.mallet_radius)
        
        if D.rink_top + D.puck_radius <= puck[1] <= D.rink_bottom - D.puck_radius:
            screen.blit(self.puck_sprite, puck - D.puck_radius)
        elif D.rink_top - D.puck_radius <= puck[1] <= D.center[1]:
            if   D.rink_top + D.puck_radius * 0.7 <= puck[1]:
                screen.blit(self.puck_sprites_top[6], puck - D.puck_radius)
            elif D.rink_top + D.puck_radius * 0.4 <= puck[1]:
                screen.blit(self.puck_sprites_top[5], puck - D.puck_radius)
            elif D.rink_top + D.puck_radius * 0.1 <= puck[1]:
                screen.blit(self.puck_sprites_top[4], puck - D.puck_radius)
            elif D.rink_top - D.puck_radius * 0.1 <= puck[1]:
                screen.blit(self.puck_sprites_top[3], puck - D.puck_radius)
            elif D.rink_top - D.puck_radius * 0.4 <= puck[1]:
                screen.blit(self.puck_sprites_top[2], puck - D.puck_radius)
            elif D.rink_top - D.puck_radius * 0.7 <= puck[1]:
                screen.blit(self.puck_sprites_top[1], puck - D.puck_radius)
            elif D.rink_top - D.puck_radius       <= puck[1]:
                screen.blit(self.puck_sprites_top[0], puck - D.puck_radius)
        elif D.center[1] <= puck[1] <= D.rink_bottom + D.puck_radius:
            if   puck[1] <= D.rink_bottom - D.puck_radius * 0.7:
                screen.blit(self.puck_sprites_bottom[6], puck - D.puck_radius)
            elif puck[1] <= D.rink_bottom - D.puck_radius * 0.4:
                screen.blit(self.puck_sprites_bottom[5], puck - D.puck_radius)
            elif puck[1] <= D.rink_bottom - D.puck_radius * 0.1:
                screen.blit(self.puck_sprites_bottom[4], puck - D.puck_radius)
            elif puck[1] <= D.rink_bottom + D.puck_radius * 0.1:
                screen.blit(self.puck_sprites_bottom[3], puck - D.puck_radius)
            elif puck[1] <= D.rink_bottom + D.puck_radius * 0.4:
                screen.blit(self.puck_sprites_bottom[2], puck - D.puck_radius)
            elif puck[1] <= D.rink_bottom + D.puck_radius * 0.7:
                screen.blit(self.puck_sprites_bottom[1], puck - D.puck_radius)
            elif puck[1] <= D.rink_bottom + D.puck_radius:
                screen.blit(self.puck_sprites_bottom[0], puck - D.puck_radius)
                
                
        screen.blit(self.top_arm_sprite, 
                    top_mallet - np.array((D.mallet_radius, self.top_arm_sprite.get_size()[1] - D.mallet_radius), dtype=np.float32))
#        screen.blit(self.bottom_arm_sprite, bottom_mallet - D.mallet_radius)

        
        pygame.draw.line(screen, (0, 0, 16), [D.rink_left, bottom_mallet[1]], [D.rink_right, bottom_mallet[1]], 24) 
        pygame.draw.line(screen, (0, 0, 16), [(D.table_left+D.rink_left)/2, D.table_bottom], [(D.table_left+D.rink_left)/2, D.center[1]], 24) 
        pygame.draw.line(screen, (0, 0, 16), [(D.table_right+D.rink_right)/2, D.table_bottom], [(D.table_right+D.rink_right)/2, D.center[1]], 24) 
 
        
        if debug:
            for line in self.borders:
                pygame.draw.line(screen, (0, 255, 255), line.p2, line.p1, 6)  
            
    def draw_collision_points(self, screen):
        import pygame
        for obj, points in self.points.items():
            radius = 6
            if obj =='p':
                color = C.puck
                radius = 10
            elif obj =='tm':
                color = C.top_mallet
            elif obj =='bm':
                color = C.bottom_mallet
            for point in points:
                pygame.draw.circle(screen, color, point, radius)  
     
    def render(self, screen, debug=0):
        if screen is None: return
        self.draw(screen, self.puck.position, self.top_mallet.position, self.bottom_mallet.position, debug)
        if debug: self.draw_collision_points(screen)
        
    # Render game after it was played
    def render_observations(self, screen, observations):
        self.draw(screen, observations[0], observations[1], observations[2])