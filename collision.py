import pygame

from vector import Vector    
        
class Collision(object):        
    @staticmethod
    def _resolve_circle_circle_velocity(dt, bodies, restitution):
        
        position_0 = bodies[0].position
        position_1 = bodies[1].position
        velocity_0 = bodies[0].get_velocity()
        velocity_1 = bodies[1].get_velocity()
        if (velocity_0 - velocity_1) * (position_0 - position_1) > 0:
            return
#            
        mass_0 = bodies[0].get_mass()
        mass_1 = bodies[1].get_mass()
        total_mass = mass_0 + mass_1
        new_velocity_0 = (velocity_0 * (mass_0 - mass_1) + (velocity_1 * 2 * mass_1)) / (total_mass)
        new_velocity_1 = (velocity_1 * (mass_1 - mass_0) + (velocity_0 * 2 * mass_0)) / (total_mass)
        
        new_velocity_0 *= restitution
        new_velocity_1 *= restitution
        
        bodies[0].set_velocity(new_velocity_0)
        bodies[1].set_velocity(new_velocity_1)
        
        bodies[0].position += bodies[0].get_velocity() * dt;
        bodies[1].position += bodies[1].get_velocity() * dt;
    
    @staticmethod
    def _resolve_circle_circle_interpenetration(dt, bodies, normal, penetration):
        if penetration <= 0.0: return
        
        total_inverse_mass  = bodies[0].get_inverse_mass() 
        total_inverse_mass += bodies[1].get_inverse_mass()
        if total_inverse_mass <= 0.0: return
        
        disposition_per_inverse_mass = normal * (penetration / total_inverse_mass)
        bodies[0].position += disposition_per_inverse_mass *  bodies[0].get_inverse_mass()
        bodies[1].position += disposition_per_inverse_mass * -bodies[1].get_inverse_mass()
        
    @staticmethod
    def circle_circle(dt, bodies, restitution):
        position_0 = bodies[0].position
        position_1 = bodies[1].position
        total_radius = bodies[0].radius + bodies[1].radius
        
        middle = position_0 - position_1
        distance = middle.magnitude()
        
        if distance <= 0.0 or distance >= (total_radius): return
        
        normal = middle * (1.0/distance)
        penetration = total_radius - distance
        
        Collision._resolve_circle_circle_velocity(dt, bodies, restitution)
        Collision._resolve_circle_circle_interpenetration(dt, bodies, normal, penetration)
        
    @staticmethod
    def circle_line(body, line):        
        relative_position = body.position - line.p1
    
        projected_vector = line.direction * (relative_position * line.direction)
        closest_point = line.p1 + projected_vector
        
        cx, cy = closest_point.get_xy()
        lx1, ly1 = line.p1.get_xy()
        lx2, ly2 = line.p2.get_xy()
        
        # Make sure that closest point lies on the line
        if lx1 - lx2 > 0: cx = max(min(cx, lx1), lx2)
        else:             cx = min(max(cx, lx1), lx2)
        if ly1 - ly2 > 0: cy = max(min(cy, ly1), ly2)
        else:             cy = min(max(cy, ly1), ly2)
        closest_point = Vector([cx, cy])
            
        distance = (body.position - closest_point).magnitude()
        if distance < body.radius:
            
            # Resovle interpenetration
            orthogonal_vector = relative_position - projected_vector
            penetration = body.radius - orthogonal_vector.magnitude()
            disposition = orthogonal_vector.normalize() * penetration
            body.position += disposition
            
            # Resolve Velocity
            velocity = body.get_velocity() - line.normal * (body.get_velocity() * line.normal) * 2 * body.wall_restitution
            body.set_velocity(velocity)