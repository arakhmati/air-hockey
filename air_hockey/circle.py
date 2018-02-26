import numpy as np
from abc import ABC
import air_hockey.vector as V
import air_hockey.phy_const as P

class Circle(ABC):
    def __init__(self, position, radius, borders, mass, maximum_speed, friction, body_restitution, wall_restitution):
        self.position = np.array(position, dtype=np.float32)
        self._velocity = np.zeros(2, dtype=np.float32)
        self.maximum_speed = maximum_speed

        if mass == 0.0:
            raise ValueError('Mass cannot be zero')
        self._inverse_mass = 1/float(mass)

        self.friction = friction
        self.accumulated_forces = np.zeros(2, dtype=np.float32)

        self.radius = radius
        self.borders = borders
        self.body_restitution = body_restitution
        self.wall_restitution = wall_restitution

    def set_velocity(self, velocity):
        magnitude = V.magnitude(velocity)
        # Limit velocity to prevent the body from escaping its borders
        if magnitude > self.maximum_speed:
            velocity *= self.maximum_speed / magnitude
        self._velocity[:] = velocity

    def get_velocity(self):
        return np.copy(self._velocity)

    def get_inverse_mass(self):
        return np.copy(self._inverse_mass)

    def add_force(self, force):
        self.accumulated_forces += force

    def clear_accumulators(self):
        self.accumulated_forces[:] = 0

    # updates position and velocity
    def integrate(self, dt):
        velocity = self._velocity + self.accumulated_forces * self._inverse_mass * dt
        velocity *= self.friction
        self.set_velocity(velocity)
        self.position += self._velocity * dt

    def reset(self, dim, top, bottom):
        self.clear_accumulators()
        self.position[:] = dim.random_position(self, top, bottom)
        self._velocity[:] = 0
        
class Target(Circle):
    def __init__(self, position, radius):
        super().__init__(position, radius, None, 1.0, 0, 0, 0, 0)
        
class Puck(Circle):
    def __init__(self, position, radius, borders):
        super().__init__(position, radius, borders, P.puck_mass,
             P.puck_maximum_speed, P.puck_friction, P.mallet_mallet_restitution, P.puck_wall_restitution)

class Mallet(Circle):
    def __init__(self, position, radius, borders):
        super().__init__(position, radius, borders, P.mallet_mass,
             P.mallet_maximum_speed, P.mallet_friction, P.puck_mallet_restitution, P.mallet_wall_restitution)

    # updates position and velocity
    def integrate(self, dt):
        velocity = self.accumulated_forces
        # velocity *= self.friction
        self.set_velocity(velocity)
        self.position += self._velocity * dt