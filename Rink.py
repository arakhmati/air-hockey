import pygame

from color_utils import colors

class Rink:
    
    def __init__(self, width, height, margin):
        self.__margin   = margin
        self.__left     = self.__margin
        self.__top      = self.__margin
        self.__right    = width - self.__margin
        self.__bottom   = height - self.__margin
        self.__width    = self.__right - self.__left
        self.__height   = self.__bottom - self.__top
        self.__center_x = width//2
        self.__center_y = height//2
        
    def get_margin(self):
        return self.__margin
    
    def get_left(self):
        return self.__left
    
    def get_top(self):
        return self.__top
    
    def get_right(self):
        return self.__right
    
    def get_bottom(self):
        return self.__bottom
    
    def get_width(self):
        return self.__width
    
    def get_height(self):
        return self.__height
    
    def get_center_x(self):
        return self.__center_x
    
    def get_center_y(self):
        return self.__center_y
    
    def draw(self, screen):
        pygame.draw.rect(screen, colors['white'], (self.__left, self.__top, self.__width, self.__height), 0)
        
        pygame.draw.line(screen,   colors['red'], [self.__left, self.__center_y], [self.__right, self.__center_y], 5)
        pygame.draw.circle(screen, colors['red'], [self.__center_x, self.__center_y], 50, 5)
        pygame.draw.circle(screen, colors['red'], [self.__center_x, self.__center_y], 10)

