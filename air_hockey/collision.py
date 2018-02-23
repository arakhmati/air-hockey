import numpy as np
import air_hockey.vector as V

class Collision(object):

    @staticmethod
    def _resolve_circle_circle_velocity(bodies, normal, restitution):
        velocity_0 = bodies[0].get_velocity()
        velocity_1 = bodies[1].get_velocity()
        inverse_mass_0 = bodies[0].get_inverse_mass()
        inverse_mass_1 = bodies[1].get_inverse_mass()

        relative_velocity  = velocity_0
        relative_velocity -= velocity_1
        separating_velocity = relative_velocity.dot(normal)
        if separating_velocity >= 0.0: return

        new_separating_velocity = -separating_velocity * restitution

        delta_velocity = new_separating_velocity - separating_velocity

        total_inverse_mass  = inverse_mass_0
        total_inverse_mass += inverse_mass_1

        impulse = delta_velocity * total_inverse_mass # FIXED BUG : Textbook had '/' instead of '*'
        impulse_per_inverse_mass = normal * impulse

        new_velocity_0 = velocity_0 + impulse_per_inverse_mass *  inverse_mass_0
        new_velocity_1 = velocity_1 + impulse_per_inverse_mass * -inverse_mass_1

        bodies[0].set_velocity(new_velocity_0)
        bodies[1].set_velocity(new_velocity_1)

    @staticmethod
    def _resolve_circle_circle_interpenetration(bodies, normal, penetration):
        if penetration <= 0.0: return

        total_inverse_mass  = bodies[0].get_inverse_mass()
        total_inverse_mass += bodies[1].get_inverse_mass()

        disposition_per_inverse_mass = normal * (penetration / total_inverse_mass)
        bodies[0].position += disposition_per_inverse_mass *  bodies[0].get_inverse_mass()
        bodies[1].position += disposition_per_inverse_mass * -bodies[1].get_inverse_mass()

    @staticmethod
    def circle_circle(bodies, resolve=True):
        restitution = max(bodies[0].body_restitution, bodies[1].body_restitution)

        position_0   = bodies[0].position
        position_1   = bodies[1].position
        total_radius = bodies[0].radius + bodies[1].radius

        direction = position_0 - position_1
        distance = V.magnitude(direction)
        if distance <= 0.0 or distance >= (total_radius):
            return False

        normal      = V.normalize(direction)
        penetration = total_radius - distance

        if resolve:
            Collision._resolve_circle_circle_velocity(bodies, normal, restitution)
            Collision._resolve_circle_circle_interpenetration(bodies, normal, penetration)

        return True

    @staticmethod
    def circle_line(body, line, screen=None):
        relative_position = body.position - line.p1

        projected_vector = line.direction * relative_position.dot(line.direction)
        closest_point = line.p1 + projected_vector

        cx, cy = closest_point
        lx1, ly1 = line.p1
        lx2, ly2 = line.p2

        # Make sure that closest point lies on the line
        if lx1 - lx2 > 0: cx = max(min(cx, lx1), lx2)
        else:             cx = min(max(cx, lx1), lx2)
        if ly1 - ly2 > 0: cy = max(min(cy, ly1), ly2)
        else:             cy = min(max(cy, ly1), ly2)
        closest_point[:] = cx, cy

        distance = V.magnitude(body.position - closest_point)
        
        collided = distance < body.radius
        if collided:

            # Resolve interpenetration
            orthogonal_vector = relative_position - projected_vector
            penetration = body.radius - V.magnitude(orthogonal_vector)
            disposition = V.normalize(orthogonal_vector) * penetration
            body.position += disposition

            # Resolve Velocity
            velocity = body.get_velocity() - line.normal * body.get_velocity().dot(line.normal) * 2 * body.wall_restitution
            body.set_velocity(velocity)

        return collided