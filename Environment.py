import pygame

from Rink import Rink
from Puck import Puck
from Mallet import KeyboardMallet, MouseMallet, CpuMallet
from GoalPosts import GoalPosts

from color_utils import colors
        
score_board = 50

class Environment:
    
    def __init__(self, width, height, margin):
        
        self.__width = width
        self.__height = height
        self.__margin = margin
        
        self.__clock = pygame.time.Clock()
        self.__screen = pygame.display.set_mode((self.__width, self.__height + score_board))
        pygame.display.set_caption("Air Hockey")
        
        self.__center_x = self.__width  // 2
        self.__center_y = self.__height // 2
        
        self.__elasticity = 0.75
        
        self.__rink = Rink(self.__width, self.__height, self.__margin)
        
        self.__goal_posts = GoalPosts(self.__center_x, self.__height, self.__margin)
        
        self.__puck = Puck((self.__center_x, self.__center_y), self.__rink, self.__goal_posts)
        
        self.__mallet_1  = MouseMallet('top', self.__rink, self.__puck)
        self.__mallet_2  = CpuMallet('bottom', self.__rink, self.__puck)
        
        
        pygame.font.init()
#        self.__font = pygame.font.SysFont("Comic Sans MS", 20)
        
        
    def update(self): 
        
        dt = self.__clock.tick(60)  
        
        for mallet in [self.__mallet_1, self.__mallet_2]:
            self.__puck.collision(mallet, dt)
        
        for obj in [self.__puck, self.__mallet_1, self.__mallet_2]:
            obj.move(dt)
        
        if self.__goal_posts.scored():
            for obj in [self.__puck, self.__mallet_1, self.__mallet_2]:
                obj.reset()
            
        self.__screen.fill(colors['black'])
        for drawable in [self.__rink, self.__goal_posts, self.__puck, self.__mallet_1, self.__mallet_2]:
            drawable.draw(self.__screen)
        
        basicfont = pygame.font.SysFont(None, 24)
        text = basicfont.render(str(self.__goal_posts.get_score()), True, (255, 255, 0))
        textrect = text.get_rect()
        textrect.centerx = self.__screen.get_rect().centerx
        textrect.centery = self.__screen.get_rect().centery
        self.__screen.blit(text, (180, self.__height + 20))
        pygame.display.flip()
    