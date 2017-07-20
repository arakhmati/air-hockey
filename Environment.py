import pygame

from Rink import Rink
from Puck import Puck
from Mallet import KeyboardMallet, MouseMallet
from GoalPosts import GoalPosts

from color_utils import colors
        

class Environment:
    
    def __init__(self, width, height, margin):
        self.__width = width
        self.__height = height
        self.__margin = margin
        
        self.__center_x = self.__width // 2
        self.__center_y = self.__height // 2
        
        self.__elasticity = 0.75
        
        self.__rink = Rink(self.__width, self.__height, self.__margin)
        
        self.__goal_posts = GoalPosts(self.__center_x, self.__height, self.__margin)
        
        self.__puck = Puck((self.__center_x, self.__center_y), self.__rink, self.__goal_posts)
        
        self.__mallet_1  = MouseMallet((self.__center_x,    self.__height-self.__margin*2), self.__rink, 'top')
        self.__mallet_2  = KeyboardMallet((self.__center_x, self.__margin*2),  self.__rink, 'bottom')
        
        self.__screen = pygame.display.set_mode((self.__width, self.__height))
        pygame.display.set_caption("Air Hockey")
        
        self.__clock = pygame.time.Clock()
        
    def update(self): 
        
        dt = self.__clock.tick(60)  
        
        for mallet in [self.__mallet_1, self.__mallet_2]:
            self.__puck.collision(mallet, dt)
        
        for mallet in [self.__puck, self.__mallet_1, self.__mallet_2]:
            mallet.move(dt)
        
        if self.__goal_posts.scored():
            for obj in [self.__puck, self.__mallet_1, self.__mallet_2]:
                obj.reset()
            print(self.__goal_posts.get_score())
            
        self.__screen.fill(colors['black'])
        for drawable in [self.__rink, self.__puck, self.__mallet_1, self.__mallet_2, self.__goal_posts]:
            drawable.draw(self.__screen)
        pygame.display.flip()
    