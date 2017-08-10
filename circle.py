import pygame
import numpy as np
from abc import ABC

from vector import Vector
    
class Circle(ABC):
    def __init__(self, position, radius, borders, mass, wall_restitution, color):
        self.position = Vector(position)
        self._velocity = Vector()
        
        self.default_position = self.position
        
        if mass == 0.0:
            raise ValueError('Mass cannot be zero')
        self._mass = mass
        self._inverse_mass = 1/float(mass)
        
        self.friction = 0.9995
        self.accumulated_forces = Vector()
        
        self.radius = radius
        self.wall_restitution = wall_restitution
        self.color = color
        self.borders = borders
        
    def set_velocity(self, velocity):
        magnitude = velocity.magnitude()
        # Limit velocity to prevent the body from escaping its borders
        if magnitude > 1:
            velocity /= magnitude
        self._velocity = velocity
        
    def get_velocity(self):
        return self._velocity
        
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
        velocity = self._velocity + self.accumulated_forces * self._inverse_mass * dt
        velocity *= np.power(self.friction, dt)
        self.set_velocity(velocity)      
        self.position += self._velocity * dt
        
    def reset(self):
        self.accumulated_forces.clear()
        self.position = self.default_position
        self._velocity = Vector()
        
class Puck(Circle):
    def __init__(self, position, radius, borders, mass=1.0, wall_restitution=0.9, color=(0,0,0)):
        super().__init__(position, radius, borders, mass, wall_restitution, color)
        
    def draw(self, screen):
        x, y = self.position.get_xy()
        pygame.draw.circle(screen, (0, 0, 0), [int(x), int(y)], self.radius, 0)
        
class Mallet(Circle):
    def __init__(self, position, radius, borders, mass=15.0, wall_restitution=0.1, color=(255, 0, 0)):
        super().__init__(position, radius, borders, mass, wall_restitution, color)
        
    def draw(self, screen):
        x, y = self.position.get_xy()
        pygame.draw.circle(screen, self.color, [int(x), int(y)],  self.radius, 0)