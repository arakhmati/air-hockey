import pygame

from MovingCircle import MovingCircle
from color_utils import colors

class Puck(MovingCircle):

    def __init__( self, pos, rink, goal, radius=15, mass=1, max_speed=0.6, friction=0.0001):
        super().__init__(pos, rink, radius, mass, max_speed, friction)
        self.__goal = goal
    
    def move(self, dt):
    
        self.friction(dt)
        
        new_pos = self.get_pos()+dt*self.get_speed()
        px, py = new_pos.get_xy()
        
        if px < self.get_rink().get_left()+self.get_radius():
            px = self.get_rink().get_left()+self.get_radius()
            self.set_speed_angle (180-self.get_speed_angle())
        elif px > self.get_rink().get_right()-self.get_radius():
            px = self.get_rink().get_right()-self.get_radius()
            self.set_speed_angle (180-self.get_speed_angle())
            
        if not (self.__goal.get_left_post()+self.get_radius()//2 < px < self.__goal.get_right_post()-self.get_radius()//2):
            if (py < self.get_rink().get_top()+self.get_radius()):
                py = self.get_rink().get_top()+self.get_radius()
                self.set_speed_angle(360-self.get_speed_angle())   
            elif (py > self.get_rink().get_bottom()-self.get_radius()):
                py = self.get_rink().get_bottom()-self.get_radius()
                self.set_speed_angle(360-self.get_speed_angle())
            
        self.set_pos_xy((px,py))
        
        if py < self.get_rink().get_top()-self.get_radius():
            self.__goal.update_score('bottom')
        elif py > self.get_rink().get_bottom()+self.get_radius():
            self.__goal.update_score('top')
    
    def draw(self, screen):
        x, y = self.get_pos().get_xy()
        pygame.draw.circle(screen, colors['black'], [int(x), int(y)], self.get_radius(), 0)
#        pygame.draw.rect(screen, colors['blue'], (275+self.get_radius(), 5, 100-self.get_radius()*2, 20), 0)
#        pygame.draw.rect(screen, colors['blue'], (275+self.get_radius(), 975, 100-self.get_radius()*2, 20), 0)

