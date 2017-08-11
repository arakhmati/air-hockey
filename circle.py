import pygame
import numpy as np
from abc import ABC

from vector import Vector
import physical_constants as P
    
class Circle(ABC):
    def __init__(self, position, radius, borders, color, mass, maximum_speed, wall_restitution):
        self.position = Vector(position)
        self._velocity = Vector()
        self.maximum_speed = maximum_speed
        
        
        self.default_position = self.position
        
        if mass == 0.0:
            raise ValueError('Mass cannot be zero')
        self._mass = mass
        self._inverse_mass = 1/float(mass)
        
        self.friction = P.friction
        self.accumulated_forces = Vector()
        
        self.radius = radius
        self.borders = borders
        self.color = color
        self.wall_restitution = wall_restitution
        
    def set_velocity(self, velocity):
        magnitude = velocity.magnitude()
        # Limit velocity to prevent the body from escaping its borders
        if magnitude > self.maximum_speed:
            velocity *= self.maximum_speed / magnitude
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
    def __init__(self, position, radius, borders, color):
        super().__init__(position, radius, borders, color, P.puck_mass, P.puck_maximum_speed, P.puck_wall_restitution)
        
class Mallet(Circle):
    def __init__(self, position, radius, borders, color):
        super().__init__(position, radius, borders, color, P.mallet_mass, P.mallet_maximum_speed, P.mallet_wall_restitution)