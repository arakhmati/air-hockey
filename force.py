import pygame
from abc import ABC, abstractmethod
from vector import Vector

DEFAULT_FACTOR = 1/50

class ForceRegistry(object):
    class Registry(object):
        def __init__(self, rigid_body, force_generator):
            self.rigid_body = rigid_body
            self.force_generator = force_generator
    
    def __init__(self):
        self.registrations = set()
    
    def add(self, rigid_body, force_generator):
        self.registrations.add(self.Registry(rigid_body, force_generator))
        
    def remove(self, rigid_body, force_generator):
        for registration in self.registrations:
            if registration.particle == rigid_body and registration.force_generator == force_generator:
                self.registrations.remove(registration)
                break
        
    def update_forces(self, dt):
        for registration in self.registrations:
            registration.force_generator.update_force(registration.rigid_body, dt)
                
    def clear(self):
        self.registrations = {}

class ForceGenerator(ABC):
    def __init__(self, factor=DEFAULT_FACTOR):
        self.factor = factor
    
    @abstractmethod
    def update_force(self, rigid_body, dt):
        pass
    
class InputForce(ForceGenerator):
    def __init__(self):
        super().__init__()
        self.force = Vector()
        
    def set_force(self, force):
        self.force = Vector(force) * self.factor
        
    def update_force(self, rigid_body, dt):
        rigid_body.add_force(self.force)
        
class RandomForce(ForceGenerator):  
    def __init__(self, factor=DEFAULT_FACTOR):
        super().__init__(factor)
        self.count = 0
        self.limit = 10
        self.force = Vector([0, 0])
        
    def update_force(self, rigid_body, dt):
        import random
        if self.count == self.limit:
           self.force =  Vector([random.randrange(-1, 2, 1)*self.factor, random.randrange(-1, 2, 1)*self.factor])
           self.count = 0
        self.count += 1
        rigid_body.add_force(self.force)
        
class KeyboardForce(ForceGenerator):  
    def __init__(self, factor=DEFAULT_FACTOR, player=0):
        super().__init__(factor)
        self.player = player
        
        
    def update_force(self, rigid_body, dt):
        if self.player == 0:
            keys = pygame.key.get_pressed()  
            if   keys[pygame.K_a]: x = -1  
            elif keys[pygame.K_d]: x =  1
            else:                  x =  0                 
            if   keys[pygame.K_w]: y = -1       
            elif keys[pygame.K_s]: y =  1     
            else:                  y =  0
        else:
            keys = pygame.key.get_pressed()  
            if   keys[pygame.K_LEFT]:  x = -1  
            elif keys[pygame.K_RIGHT]: x =  1
            else:                      x =  0                 
            if   keys[pygame.K_UP]:    y = -1       
            elif keys[pygame.K_DOWN]:  y =  1     
            else:                      y =  0
            
        self.force =  Vector([x*self.factor, y*self.factor])
        rigid_body.add_force(self.force)