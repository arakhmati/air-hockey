import pygame

from color_utils import colors

class Goal(object):
    def __init__(self,center_x,center_y,w=100,h=20):
        self.center_x = center_x
        self.center_y = center_y
        self.w = w
        self.h = h
        
        self.x = self.center_x - self.w/2
        self.y = self.center_y - self.h/2
        
        self.start = self.x
        self.end = self.x + self.w
                
    def draw(self, screen):
        pygame.draw.rect(screen, colors['green'], (self.x,self.y,self.w,self.h), 0)