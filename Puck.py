import pygame

import ActiveCircle
from color_utils import colors

class Puck(ActiveCircle.ActiveCircle):

    def __init__( self, pos, rink, goal, radius=15, angle=0, magnitude=0, mass=1, max_speed=0.6, friction=0.0001):
        ActiveCircle.ActiveCircle.__init__( self, pos, radius, angle, magnitude, mass, max_speed)
        self.__friction = friction
        self.left = rink.left
        self.top = rink.top
        self.right = rink.right
        self.bottom = rink.bottom
        
        if goal is not None:
            self.goal_start = goal.start
            self.goal_end = goal.end
        
    def get_friction(self):
        return self.__friction
        
    def set_friction(self,friction):
        self.__friction = friction
                
    def friction( self, dt):
        if self.get_speed_magnitude()>0:
            self.set_speed_magnitude(self.get_speed_magnitude()-self.get_friction()*dt)
        if self.get_speed_magnitude()<0:
            self.set_speed_magnitude(0)
        
    def mod(self, dt):
        self.friction(dt)
        
    def move(self, dt):
    
        new_pos = self.get_pos()+dt*self.get_speed()
        px, py = new_pos.get_xy()
        
        if px < self.left+self.get_radius()*0.5:
            px = self.left+self.get_radius()*0.5
            self.set_speed_angle (180-self.get_speed_angle())
        elif px > self.right-self.get_radius()*0.5:
            px = self.right-self.get_radius()*0.5
            self.set_speed_angle (180-self.get_speed_angle())
            
        if not (self.goal_start < px < self.goal_end):
            if (py < self.top+self.get_radius()*0.5):
                py = self.top+self.get_radius()*0.5
                self.set_speed_angle(360-self.get_speed_angle())   
            elif (py > self.bottom-self.get_radius()*0.5):
                py = self.bottom-self.get_radius()*0.5
                self.set_speed_angle(360-self.get_speed_angle())
            
        self.set_pos_xy((px,py))
        
        if py < self.top-self.get_radius():
            return 'player'
        elif py > self.bottom+self.get_radius():
            return 'cpu'
        
        return ''
    
    def draw(self, screen):
        x, y = self.get_pos().get_xy()
        pygame.draw.circle(screen, colors['black'], [int(x), int(y)], 15, 0)