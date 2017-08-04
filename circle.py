import pygame
import numpy as np
from abc import ABC

from vector import Vector
    
class Circle(ABC):
    def __init__(self, position, radius, mass, wall_restitution):
        self.position = Vector(position)
        self.velocity = Vector()
        
        self._mass = mass
        self._inverse_mass = 1/float(mass)
        self.friction = 0.9995
        
        self.accumulated_forces = Vector()
        
        self.radius = radius
        self.wall_restitution = -wall_restitution
    
    def set_mass(self, mass):
        self.mass = mass
        if mass == 0.0:
            raise  ValueError('Mass cannot be zero')
        self.inverse_mass = 1/mass
    
    def get_mass(self):
        return self._mass
    
    def get_inverse_mass(self):
        return self._inverse_mass
    
        
    def add_force(self, force):
        self.accumulated_forces += force
        
    def clear_accumulators(self):
        self.accumulated_forces.clear()        
        
    # updates position and velocity
    def integrate(self, dt):
        self.velocity += self.accumulated_forces * self._inverse_mass * dt
        self.velocity *= np.power(self.friction, dt)        
        self.position += self.velocity * dt
        
class Puck(Circle):
    def __init__(self, position, radius, mass=1.0, wall_restitution=0.9):
        super().__init__(position, radius, mass, wall_restitution)
        
    def draw(self, screen):
        x, y = self.position.get_xy()
        pygame.draw.circle(screen, (0, 0, 0), [int(x), int(y)], self.radius, 0)
        
class Mallet(Circle):
    def __init__(self, position, radius, mass=15.0, wall_restitution=0.1, color=(255, 0, 0)):
        super().__init__(position, radius, mass, wall_restitution)
        self.color = color
        
    def draw(self, screen):
        x, y = self.position.get_xy()
        pygame.draw.circle(screen, self.color, [int(x), int(y)],  self.radius, 0)