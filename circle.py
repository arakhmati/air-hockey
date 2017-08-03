import pygame

from abc import ABC

from vector import Vector
    
class Particle(ABC):
    def __init__(self, position, mass):
        self.position = Vector(position)
        self.velocity = Vector()
        self.acceleration = Vector()
        
        self.mass = mass
        self._inverse_mass = 1/float(mass)
        self.friction = 0.98
        self.wall_restitution = -1
        
        self.accumulated_forces = Vector()
        
    def set_position(self, position):
        self.position = position
        
    def set_velocity(self, velocity):
        self.velocity = velocity
        
    def set_acceleration(self, acceleration):
        self.acceleration = acceleration
    
    def set_mass(self, mass):
        self.mass = mass
        if mass == 0.0:
            raise  ValueError('Mass cannot be zero')
        self.inverse_mass = 1/mass
    
    def get_position(self):
        return self.position
    
    def get_velocity(self):
        return self.velocity
    
    def get_acceleration(self):
        return self.acceleration
    
    def get_inverse_mass(self):
        return self._inverse_mass
    
        
    def add_force(self, force):
        self.accumulated_forces += force
        
    def clear_accumulators(self):
        self.accumulated_forces.clear()        
        
    # updates position and velocity
    def integrate(self, dt):
        
        last_frame_acceleration = self.acceleration + self.accumulated_forces * self._inverse_mass
        
        self.velocity += last_frame_acceleration * dt
#        self.velocity *= np.power(self.friction, dt)
        self.velocity *= self.friction
        if self.velocity.magnitude() < 0.01:
            self.velocity = Vector([0, 0])
        
        self.position += self.velocity * dt
        
class Circle(Particle, ABC):
    def __init__(self, position, radius, mass, wall_restitution):
        super().__init__(position, mass)
        self.radius = radius
        self.wall_restitution = -wall_restitution
        
    def integrate(self, dt):
        
        super().integrate(dt)
        
        px, py = self.position.v
        if px < 25 + self.radius:
            px = 25 + self.radius
            self.velocity.v[0] *= self.wall_restitution
#            touched = True
        elif px > 475 - self.radius:
            px = 475 - self.radius
            self.velocity.v[0] *= self.wall_restitution
#            touched = True
        
        if py < 25 + self.radius:
            py = 25 + self.radius
            self.velocity.v[1] *= self.wall_restitution
#            touched = True
        elif py > 675 - self.radius:
            py = 675 -+ self.radius
            self.velocity.v[1] *= self.wall_restitution
            
        self.position = Vector([px, py])
        
class Disc(Circle):
    def __init__(self, position, radius, mass=1.0, wall_restitution=0.9):
        super().__init__(position, radius, mass, wall_restitution)
        
    def draw(self, screen):
        x, y = self.get_position().v
        pygame.draw.circle(screen, (0, 0, 0), [int(x), int(y)], self.radius, 0)
        
class Mallet(Circle):
    def __init__(self, position, radius, mass=15.0, wall_restitution=0.1, color=(255, 0, 0)):
        super().__init__(position, radius, mass, wall_restitution)
        import random
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
    def draw(self, screen):
        x, y = self.get_position().v
        pygame.draw.circle(screen, self.color, [int(x), int(y)],  self.radius, 0)