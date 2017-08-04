from vector import Vector    
        
class Contact(object):
    def __init__(self, bodies, normal, penetration, restitution):
        self.bodies      = bodies
        self.normal      = normal
        self.penetration = penetration
        self.restitution = restitution
        
    def _resolve_velocity(self, dt):
        
        position_0 = self.bodies[0].position
        position_1 = self.bodies[1].position
        velocity_0 = self.bodies[0].velocity
        velocity_1 = self.bodies[1].velocity
        if (velocity_0 - velocity_1) * (position_0 - position_1) > 0:
            return
#            
        mass_0 = self.bodies[0].get_mass()
        mass_1 = self.bodies[1].get_mass()
        total_mass = mass_0 + mass_1
        self.bodies[0].velocity = (velocity_0 * (mass_0 - mass_1) + (velocity_1 * 2 * mass_1)) / (total_mass)
        self.bodies[1].velocity = (velocity_1 * (mass_1 - mass_0) + (velocity_0 * 2 * mass_0)) / (total_mass)
        
        self.bodies[0].velocity *= self.restitution
        self.bodies[1].velocity *= self.restitution
        
        self.bodies[0].position += self.bodies[0].velocity * dt;
        self.bodies[1].position += self.bodies[1].velocity * dt;
    
            
    def _resolve_interpenetration(self, dt):
        if self.penetration <= 0.0:
            return
        
        total_inverse_mass  = self.bodies[0].get_inverse_mass() 
        total_inverse_mass += self.bodies[1].get_inverse_mass()
        if total_inverse_mass <= 0.0: 
            return
        
        disposition_per_inverse_mass = self.normal * (self.penetration / total_inverse_mass)
        
        self.bodies[0].position += disposition_per_inverse_mass *  self.bodies[0].get_inverse_mass()
        self.bodies[1].position += disposition_per_inverse_mass * -self.bodies[1].get_inverse_mass()
        
    def resolve(self, dt):
        self._resolve_velocity(dt)
        self._resolve_interpenetration(dt)