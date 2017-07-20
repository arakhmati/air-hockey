import pygame

from Vector import Vector
from MovingCircle import MovingCircle
from physics_utils import angle_from_O, distance_from_O
from color_utils import colors

class Mallet(MovingCircle):
    def __init__( self, pos, rink, player, radius=20, mass=1, max_speed=0.6, acceleration=0.0025, friction=0.0001):
        super().__init__(pos, rink, radius, mass, max_speed, friction)
        self.__acceleration = acceleration
        self.__player = player
        
        if self.get_player() == 'top':
            self.__top_bound    = self.get_rink().get_top()+0.5*(self.get_rink().get_height())+self.get_radius()
            self.__bottom_bound = self.get_rink().get_top()+self.get_rink().get_height()-self.get_radius()
        else:
            self.__top_bound    = self.get_rink().get_top()+self.get_radius()
            self.__bottom_bound = self.get_rink().get_top()+0.5*(self.get_rink().get_height())-self.get_radius()
        
    def get_acceleration(self):
        return self.__acceleration

    def get_player(self):
        return self.__player
            
    def set_acceleration(self,acceleration):
        self.__acceleration = acceleration

    def set_player(self,player):
        self.__player = player

    def move(self, new_pos, vx, vy):
 
        self.set_speed_angle(angle_from_O((vx, vy)))
        new_speed = distance_from_O((vx, vy))
        self.set_speed_magnitude (min(new_speed, self.get_max_speed()))
        
        px, py = new_pos.get_xy()
        
        if (px < self.get_rink().get_left()+self.get_radius()):
            px = self.get_rink().get_left()+self.get_radius()
        elif (px > self.get_rink().get_right()-self.get_radius()):
            px = self.get_rink().get_right()-self.get_radius()
        
        if (py < self.__top_bound):
            py = self.__top_bound
        elif (py > self.__bottom_bound):
            py = self.__bottom_bound
        
        self.set_pos_xy((px, py))
        
    def draw( self, screen):
        x, y = self.get_pos().get_xy()
        pygame.draw.circle(screen, colors['red'],   [int(x), int(y)], 20, 0)
        pygame.draw.circle(screen, colors['black'], [int(x), int(y)], 20, 1)
        pygame.draw.circle(screen, colors['black'], [int(x), int(y)], 5,  0)
        
class KeyboardMallet(Mallet):
    def move( self, dt):
        keys = pygame.key.get_pressed()  
        if keys[pygame.K_a]: x = -1.0    
        elif keys[pygame.K_d]: x = 1.0  
        else: x = 0.0                  
        if keys[pygame.K_w]: y = -1.0          
        elif keys[pygame.K_s]: y = 1.0       
        else: y = 0.0

        self.friction(dt)
    
        vx, vy = self.get_speed_xy()
        vx += x*self.get_acceleration()*dt
        vy += y*self.get_acceleration()*dt
        
        super().move(self.get_pos()+dt*self.get_speed(), vx, vy)
        
class MouseMallet(Mallet):
    def move(self, dt):
        new_pos = pygame.mouse.get_pos()
        new_pos = Vector(angle_from_O(new_pos), distance_from_O(new_pos))
        new_px, new_py = new_pos.get_xy()
        px, py = self.get_pos_xy()
        vx = new_px - px
        vy = new_py - py
        super().move(new_pos, vx, vy)
        
#class MouseMallet(Mallet):
#    
#    def __init__( self, pos, rink, player, radius=20, mass=1, max_speed=0.6, acceleration=0.0025, friction=0.0001):
#        
#        super().__init__(pos, rink, player, radius, mass, max_speed, acceleration, friction)
#    def move(self, dt):
#        new_pos = pygame.mouse.get_pos()
#        new_pos = Vector(angle_from_O(new_pos), distance_from_O(new_pos))
#        new_px, new_py = new_pos.get_xy()
#        px, py = self.get_pos_xy()
#        vx = new_px - px
#        vy = new_py - py
#        super().move(new_pos, vx, vy)

        
    
