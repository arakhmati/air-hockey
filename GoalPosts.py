import pygame

from color_utils import colors

class GoalPosts(object):
    def __init__(self, center_x, bottom, margin, width=100, height=20):
        self.__center_x = center_x
        self.__bottom = bottom
        self.__width = width
        self.__height = height
        self.__top_y = (margin - self.__height)
        self.__bottom_y = self.__bottom - self.__height - self.__top_y
        
        self.__left = self.__center_x - self.__width/2        
        self.__right = self.__left + self.__width
        
        self.__score = {'top': 0, 'bottom': 0}
        self.__scored = False
        
    def get_left_post(self):
        return self.__left
    
    def get_right_post(self):
        return self.__right
    
    def update_score(self, post):
        self.__score[post] += 1
        self.__scored = True
        
    def scored(self):
        return self.__scored
    
    def get_score(self):
        self.__scored = False
        return self.__score
                
    def draw(self, screen):
        pygame.draw.rect(screen, colors['green'], (self.__left, self.__top_y,    self.__width, self.__height), 0)
        pygame.draw.rect(screen, colors['green'], (self.__left, self.__bottom_y, self.__width, self.__height), 0)