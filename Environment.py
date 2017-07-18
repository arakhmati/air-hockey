import pygame

from Rink import Rink
from Puck import Puck
from Mallet import Mallet
from Goal import Goal

from color_utils import colors
        

class Environment:
    
    def __init__(self, width, height, margin):
        self.width = width
        self.height = height
        self.margin = margin
        
        self.elasticity = 0.75
        
        self.rink = Rink(width, height, margin)
        
        
        self.playerGoal = Goal(250, 685)
        self.cpuGoal    = Goal(250, 15)
        
        self.puck = Puck((250, 350), self.rink, self.playerGoal)
        
        self.playerMallet = Mallet((250, 650), self.rink, 'player')
        self.cpuMallet    = Mallet((250, 50),  self.rink, 'cpu')
        
        self.score = {'player': 0, 'cpu': 0}
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Air Hockey")
        
        self.clock = pygame.time.Clock()
        
    def update(self): 
        
        dt = self.clock.tick(60)  
        
        (mouseX, mouseY) = pygame.mouse.get_pos()
    
        keys = pygame.key.get_pressed()
        if keys[ pygame.K_LEFT]: x1 = -1.0    
        elif keys[ pygame.K_RIGHT]: x1 = 1.0  
        else: x1 = 0.0                  
        if keys[pygame. K_UP]: y1 = -1.0          
        elif keys[ pygame.K_DOWN]: y1 = 1.0       
        else: y1 = 0.0     
        if keys[ pygame.K_a]: x2 = -1.0    
        elif keys[ pygame.K_d]: x2 = 1.0  
        else: x2 = 0.0                  
        if keys[ pygame.K_w]: y2 = -1.0          
        elif keys[ pygame.K_s]: y2 = 1.0       
        else: y2 = 0.0
        
        self.playerMallet.mod(x1, y1, dt)
        self.cpuMallet.mod(x2, y2, dt)
        self.puck.mod(dt)
        
        self.puck.collision(self.playerMallet, dt)
        self.puck.collision(self.cpuMallet, dt)
        
        self.playerMallet.move(dt)
        self.cpuMallet.move(dt)
        result = self.puck.move(dt)
        
        if result != '':
            self.puck.reset()
            self.cpuMallet.reset()
            self.playerMallet.reset()
            self.score[result] += 1
            print(self.score)
            
        self.screen.fill(colors['black'])
        for drawable in [self.rink, self.puck, self.playerMallet, self.cpuMallet, self.playerGoal, self.cpuGoal]:
            drawable.draw(self.screen)
        pygame.display.flip()
    