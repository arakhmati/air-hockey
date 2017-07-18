import pygame

from color_utils import colors

class Rink:
    
    def __init__(self, width, height, margin):
        self.margin   = margin
        self.left     = self.margin
        self.top      = self.margin
        self.right    = width - self.margin
        self.bottom   = height - self.margin
        self.width    = self.right - self.left
        self.height   = self.bottom - self.top
        self.center_x = width//2
        self.center_y = height//2
        
    def draw(self, screen):
        pygame.draw.rect(screen, colors['white'], (self.left, self.top, self.width, self.height), 0)
        
        pygame.draw.line(screen,   colors['red'], [self.left, self.center_y], [self.right, self.center_y], 5)
        pygame.draw.circle(screen, colors['red'], [self.center_x, self.center_y], 50, 5)
        pygame.draw.circle(screen, colors['red'], [self.center_x, self.center_y], 10)

