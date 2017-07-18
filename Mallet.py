import pygame

import Puck
from physics_utils import angle_from_O, distance_from_O, angle, distance

from color_utils import colors


class Mallet(Puck.Puck):

    def __init__( self, pos, rink, player, radius=20, mass=1, max_speed=0.6, acceleration=0.0025, friction=0.0001):
        Puck.Puck.__init__( self, pos, rink, None, radius, 0, 0, mass, max_speed, friction)
        self.__acceleration = acceleration
        self.__player = player
        self.__point = 0
        self.height = rink.height
        
        if self.get_player() == 'cpu':
            self.bottom = self.top+self.height-self.get_radius()
            self.top    = self.top+0.5*(self.height)+self.get_radius()
        else:
            self.bottom = self.top+0.5*(self.height)-self.get_radius()
            self.top    = self.top+self.get_radius()
        
    def get_acceleration(self):
        return self.__acceleration

    def get_player(self):
        return self.__player

    def get_point(self):
        return self.__point
            
    def set_acceleration(self,acceleration):
        self.__acceleration = acceleration

    def set_player(self,player):
        self.__player = player

    def set_point(self,point):
        self.__point = point   
        
    def inc_point(self):
        self.__point += 1

    def mod( self, x, y, dt):

        Puck.Puck.friction(self, dt)
    
        vx,vy = self.get_speed_xy()
        vx += x*self.get_acceleration()*dt
        vy += y*self.get_acceleration()*dt
        
        self.set_speed_angle(angle_from_O((vx,vy)))
        
        new_speed = distance_from_O((vx,vy))
        if new_speed<=self.get_max_speed():
            self.set_speed_magnitude (new_speed)

    def move(self, dt):
        touched = False
 
        new_pos = self.get_pos()+dt*self.get_speed()
        px,py = new_pos.get_xy()
        
        if (px < self.left+self.get_radius()):
            touched = True
            px = self.left+self.get_radius()
        elif (px > self.right-self.get_radius()):
            touched = True
            px = self.right-self.get_radius()
        
        if (py < self.top):
            touched = True
            py = self.top
        elif (py > self.bottom):
            touched = True
            py = self.bottom
            
        if touched:
            old_pos = self.get_pos_xy()
            self.set_speed_angle(angle(old_pos,(px,py)))
            self.set_speed_magnitude(distance(old_pos,(px,py))/dt)
        
        self.set_pos_xy((px,py))
        
    def __str__(self):
        return "P"+str(self.get_player())+": "+str(self.get_point())
        
    def draw( self, screen):
        x, y = self.get_pos().get_xy()
        pygame.draw.circle(screen, colors['red'],   [int(x), int(y)], 20, 0)
        pygame.draw.circle(screen, colors['black'], [int(x), int(y)], 20, 1)
        pygame.draw.circle(screen, colors['black'], [int(x), int(y)], 5,  0)
