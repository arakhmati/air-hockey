import numpy as np
import numbers

import pygame

from abc import ABC, abstractmethod


class Vector(object):
    def __init__(self, v=np.zeros(2)):
        self.n = len(v)
        if isinstance(v, list):
            self.v = np.array(v, dtype=np.float)
        elif isinstance(v, np.ndarray):
            self.v = v
        
    def magnitude(self):
        return np.linalg.norm(self.v)
    
    def squar_magnitude(self):
        return np.sum(np.transpose(self.v) * self.v)
    
    def normalize(self):
        mag = self.magnitude()
        
        if mag != 0.0:
            self.v /= mag
        
    def __add__(self, vector):
        return Vector(self.v + vector.v)
    
    def add(self, vector):
        self.v += vector.v
        
    def __sub__(self, vector):
        return Vector(self.v - vector.v)
    
    def sub(self, vector):
        self.v -= vector.v
        
    def __str__(self):
        return str(self.v[0]) + ' ' + str(self.v[1])
    
            
    def __mul__(self, b):
        if isinstance(b, numbers.Number): # scalar
            return Vector(self.v * b)
        elif isinstance(b, Vector):       # vector -> dot product
            return self.v.dot(b.v)
    
    def mul(self, scalar):
        self.v *= scalar
        
    def clear(self):
        self.v = np.zeros(self.n, dtype=np.float)
    
class Particle(ABC):
    def __init__(self, position, mass):
        self.position = position
        self.velocity = Vector()
        self.acceleration = Vector()
        
        self._inverse_mass = 1/float(mass)
        self.friction = 0.995
        
        self.accumulated_forces = Vector()
        
    def set_position(self, position):
        self.position = position
        
    def set_velocity(self, velocity):
        self.velocity = velocity
        
    def set_acceleration(self, acceleration):
        self.acceleration = acceleration
    
    def set_mass(self, mass):
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
        self.velocity *= np.power(self.friction, dt)
        
        self.position += self.velocity * dt
        
class RigidObject(Particle):
    def __init__(self, position, mass):
        super().__init__(Vector(position), mass)
        
class Circle(RigidObject):
    def __init__(self, position, radius, mass):
        super().__init__(position, mass)
        self.radius = radius
        
    def integrate(self, dt):
        
        super().integrate(dt)
        
        px, py = self.position.v
        if px < 25 + self.radius:
            px = 25 + self.radius
#            touched = True
        elif px > 475 - self.radius:
            px = 475 - self.radius
#            touched = True
        
        if py < 25 + self.radius:
            py = 25 + self.radius
#            touched = True
        elif py > 675 - self.radius:
            py = 675 -+ self.radius
            
        self.position = Vector([px, py])
        
class Disc(Circle):
    def __init__(self, position, radius, mass=1.0):
        super().__init__(position, radius, mass)
        
    def draw(self, screen):
        x, y = self.get_position().v
        pygame.draw.circle(screen, (0, 0, 0), [int(x), int(y)], self.radius, 0)
        
class Mallet(Circle):
    def __init__(self, position, radius, mass=15.0):
        super().__init__(position, radius, mass)
        
    def draw(self, screen):
        x, y = self.get_position().v
        pygame.draw.circle(screen, (255, 0, 0), [int(x), int(y)], self.radius, 0)
        pygame.draw.circle(screen, (0,   0, 0), [int(x), int(y)], self.radius, 1)
        pygame.draw.circle(screen, (0,   0, 0), [int(x), int(y)], 5,  0)
        
class Plane():
    def __init__(self, normal, offset):
        self.normal = normal
        self.offset = offset
        
class ForceGenerator(ABC):
    @abstractmethod
    def update_force(self, rigid_body, dt):
        pass
    
class ConstantForce(ForceGenerator):
    def __init__(self, force):
        self.force = Vector(force)
        
    def update_force(self, rigid_body, dt):
        rigid_body.add_force(self.force)
        
class RandomForce(ForceGenerator):  
    def __init__(self, factor):
        self.factor = factor
        self.count = 0
        self.limit = 100
        self.force = Vector([0, 0])
        
    def update_force(self, rigid_body, dt):
        import random
        if self.count == self.limit:
           self.force =  Vector([random.randrange(-1, 2, 1)*self.factor, random.randrange(-1, 2, 1)*self.factor])
           self.count = 0
        self.count += 1
        rigid_body.add_force(self.force)
    
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
 
class CollisionDetector(object):
    def circle_and_circle(self, circle_1, circle_2, restitution=1):
        position_1 = circle_1.get_position()
        position_2 = circle_2.get_position()
        
        middle = position_1 - position_2
        distance = middle.magnitude()
        
        if distance <= 0.0 or distance > (circle_1.radius + circle_2.radius):
            return (False, None)
        
        normal = middle * (1.0/distance)
        point = position_1 + middle*0.5
        penetration = circle_1.radius + circle_2.radius - distance
        
        if penetration > 5:
            print('circle_and_circle ' + str(penetration))
            
        penetration = min(10, penetration)
        
        contact = Contact((circle_1, circle_2), normal, point, penetration, restitution)
        return (True, contact)
    
    def circle_and_plane(self, circle, plane, restitution=1):
        position = circle.get_position()
        
        ball_distance = plane.normal * position - circle.radius - plane.offset
        
        if ball_distance >= 0.0:
            return (False, None)
        
        normal = plane.normal
        point = position - plane.normal * (ball_distance + circle.radius)
        penetration = -ball_distance
        
        if penetration > 5:
            print('circle_and_plane ' + str(penetration))
        penetration = min(10, penetration)
#        
        contact = Contact((circle, None), normal, point, penetration, restitution)
        return (True, contact)        
        
class Contact(object):
    def __init__(self, bodies, normal, point, penetration, restitution):
        self.particles   = bodies
        self.normal      = normal * -1
        self.point       = point
        self.penetration = penetration
        self.restitution = restitution
        
    def compute_separating_velocity(self):
        relative_velocity = self.particles[0].get_velocity()
        if self.particles[1]: 
            relative_velocity -= self.particles[1].get_velocity()
        return relative_velocity * self.normal
    
    def _compute_total_inverse_mass(self):
        total_inverse_mass = self.particles[0].get_inverse_mass()
        if self.particles[1]: 
            total_inverse_mass += self.particles[1].get_inverse_mass()
        return total_inverse_mass
        
    def _resolve_velocity(self, dt):
        separating_velocity = self.compute_separating_velocity()
        if separating_velocity > 0.0:
            return
        
        new_separating_velocity = -separating_velocity * self.restitution
        
        velocity_due_to_acceleration = self.particles[0].get_acceleration()
        if self.particles[1]:
            velocity_due_to_acceleration -= self.particles[1].get_acceleration()
        separating_velocity_due_to_acceleration = velocity_due_to_acceleration * self.normal * dt
        
        if separating_velocity_due_to_acceleration < 0:
            new_separating_velocity += self.restitution * separating_velocity_due_to_acceleration
            new_separating_velocity = max(new_separating_velocity, 0.0)
        
        delta_velocity = new_separating_velocity - separating_velocity
        
        total_inverse_mass = self._compute_total_inverse_mass()
        if total_inverse_mass <= 0.0: 
            return
        
        impulse = delta_velocity / total_inverse_mass
        impulse_per_inverse_mass = self.normal * impulse
        
        self.particles[0].set_velocity(self.particles[0].get_velocity() + impulse_per_inverse_mass * self.particles[0].get_inverse_mass())
        if self.particles[1]:
            self.particles[1].set_velocity(self.particles[1].get_velocity() + impulse_per_inverse_mass * -self.particles[1].get_inverse_mass())
            
    def _resolve_interpenetration(self, dt):
        if self.penetration <= 0.0:
            return
        
        total_inverse_mass = self._compute_total_inverse_mass()
        if total_inverse_mass <= 0.0: 
            return
        
        disposition_per_inverse_mass = self.normal * (-self.penetration / total_inverse_mass)
        
        self.particles[0].set_position(self.particles[0].get_position() + \
            disposition_per_inverse_mass * self.particles[0].get_inverse_mass())
        if self.particles[1]:
            self.particles[1].set_position(self.particles[1].get_position() + \
                disposition_per_inverse_mass * self.particles[1].get_inverse_mass())
        
    def resolve(self, dt):
        self._resolve_velocity(dt)
        self._resolve_interpenetration(dt)
        
class ContactResolver(object):
    def __init__(self):
        self.iterations = 10
        self.iterations_used = 0
        
    def set_iterations(self, iterations):
        self.iterations = iterations
        
    def resolve_contacts(self, contacts, dt):
        self.iterations_used = 0
        for self.iterations_used in range(self.iterations):
            if len(contacts) == 0: return
            max_value = 0.0
            max_index = 0
            for i in range(len(contacts)):
                value = contacts[i].compute_separating_velocity()
                if value > max_value:
                    max_value = value
                    max_index = i
            contacts[max_index].resolve(dt)
#        print(self.iterations_used)
            
class World(object):
    def __init__(self):
        self.objects = [Disc([250, 350], 25), Mallet([250, 125], 25), Mallet([250, 575], 25)]
        
        self.forces = ForceRegistry()
        for obj in self.objects[1:]:
            self.forces.add(obj, RandomForce(1/50))
            
        left_plane   = Plane(Vector([ 1,  0]),  25)
        top_plane    = Plane(Vector([ 0,  1]),  25)
        right_plane  = Plane(Vector([-1,  0]), -475)
        bottom_plane = Plane(Vector([ 0, -1]), -675)
        self.planes = [left_plane, top_plane, right_plane, bottom_plane]
        
        self.collision_detector = CollisionDetector()
        self.contact_resolver = ContactResolver()       

    def start_frame(self):
        for body in self.bodies:
            body.clear_accumulators()
            
    def run_physics(self, dt):
        for body in self.bodies:
            body.integrate(dt)
            
    def update(self, dt, screen):
        
        for obj in self.objects:
            obj.clear_accumulators()
            
        self.forces.update_forces(dt)
        
        for obj in self.objects:
            obj.draw(screen)
            obj.integrate(dt)
            print(obj.velocity)
#            print(obj.position)
            
        contacts = []
        for i in range(len(self.objects)):
            for j in range(i, len(self.objects)):
                if i == j: continue
                collision, contact = self.collision_detector.circle_and_circle(self.objects[i], self.objects[j])
                if collision:  contacts.append(contact)
                
        self.contact_resolver.resolve_contacts(contacts, dt)
                    
            
    
    
if __name__ == "__main__":

    pygame.init()
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((500, 700))
    
    env = World()

    done = False
    while not done:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
        dt = clock.tick_busy_loop(120)
        
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (25, 25, 450, 650), 0)
        env.update(dt, screen)
        
        pygame.display.update()
    
    
    pygame.quit ()       
    