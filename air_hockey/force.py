import pygame
import numpy as np
from abc import ABC, abstractmethod
import air_hockey.phy_const as P

class ForceRegistry(object):
    class Registry(object):
        def __init__(self, body, force_generator):
            self.body = body
            self.force_generator = force_generator
    
    def __init__(self):
        self.registrations = set()
    
    def add(self, body, force_generator):
        self.registrations.add(self.Registry(body, force_generator))
        
    def remove(self, body, force_generator):
        for registration in self.registrations:
            if registration.particle == body and registration.force_generator == force_generator:
                self.registrations.remove(registration)
                break
        
    def update_forces(self):
        for registration in self.registrations:
            registration.force_generator.update_force(registration.body)
                
    def clear(self):
        self.registrations = {}

class ForceGenerator(ABC):
    def __init__(self, factor=P.force_multiplier):
        self.factor = factor
    
    @abstractmethod
    def update_force(self, body):
        pass
    
class ControlledForce(ForceGenerator):
    def __init__(self):
        super().__init__()
        self.force = np.zeros(2, dtype=np.float32)
        
    def set_force(self, force):
        self.force[:] = force
        
    def update_force(self, body):
        body.add_force(self.force * self.factor)
        
class RandomForce(ForceGenerator):  
    def __init__(self, factor=P.force_multiplier):
        super().__init__(factor)
        self.count = 0
        self.limit = 10
        self.force = np.array([0, 0], dtype=np.float32)
        
    def update_force(self, body):
        import random
        if self.count == self.limit:
           self.force[:] = random.randrange(-1, 2, 1)*self.factor, random.randrange(-1, 2, 1)*self.factor
           self.count = 0
        self.count += 1
        body.add_force(self.force)
        
class PlayerForce(ForceGenerator):  
    def __init__(self, factor=P.force_multiplier, player=0):
        super().__init__(factor)
        self.player = player
        self.force = np.array([0, 0], dtype=np.float32)
        self.prev_x, self.prev_y = 0, 0
        
    def update_force(self, body):
        if self.player == 0:
            keys = pygame.key.get_pressed()  
            if   keys[pygame.K_a]: x = -1  
            elif keys[pygame.K_d]: x =  1
            else:                  x =  0                 
            if   keys[pygame.K_w]: y = -1       
            elif keys[pygame.K_s]: y =  1     
            else:                  y =  0
        elif self.player == 1:
            keys = pygame.key.get_pressed()  
            if   keys[pygame.K_LEFT]:  x = -1  
            elif keys[pygame.K_RIGHT]: x =  1
            else:                      x =  0                 
            if   keys[pygame.K_UP]:    y = -1       
            elif keys[pygame.K_DOWN]:  y =  1     
            else:                      y =  0
            
        self.force[:] = x*self.factor, y*self.factor
        body.add_force(self.force)