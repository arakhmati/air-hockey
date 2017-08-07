import pygame

from vector import Vector
import numpy as np
from circle import Puck, Mallet
from force import ForceRegistry, RandomForce, KeyboardForce, InputForce
from contact import Contact
from ai import RuleBasedAI, MachineLearningAI
          
class World(object):
    def __init__(self):
        self.bodies = []
#        self.bodies = [Puck([250, 350], 25), Mallet([250, 125], 25), Mallet([250, 375], 25)]
        
#        self.ai = MachineLearningAI(self.bodies[2], self.bodies[0])
        
        for i in range(125, 700, 600):
            for j in range(125, 900, 700):
                import random
                if i == 125 and j == 125:
                    self.bodies.append(Mallet((i, j), 25))
                else:
                    self.bodies.append(Mallet((i, j), 25) if random.randint(0,1) == 0 else Puck((i, j), 25))
        
#        self.aiforce = InputForce()
        self.forces = ForceRegistry()
#        self.forces.add(self.bodies[2], self.aiforce)
        self.forces.add(self.bodies[0], KeyboardForce())
        for body in self.bodies[1:]:
            if isinstance(body, Mallet):
                self.forces.add(body, RandomForce())

    @staticmethod
    def corner_collision(body, screen):
        for i in range(4):
            if i == 0:
                p0 = Vector([125, 25]) 
                p1 = Vector([25,  25])
                p2 = Vector([25, 125])
            
            elif i == 1:
                p0 = Vector([475, 125]) 
                p1 = Vector([475, 25])
                p2 = Vector([375, 25])
#                continue
            
            elif i == 2:
                p0 = Vector([375, 675]) 
                p1 = Vector([475, 675])
                p2 = Vector([475, 575])
#                continue
            
            elif i == 3:
                p0 = Vector([25,  575]) 
                p1 = Vector([25,  675])
                p2 = Vector([125, 675])
            
            x0, y0 = p0.get_xy()
            x1, y1 = p1.get_xy()
            x2, y2 = p2.get_xy()
            
            step = 0.1
            points = []
            # Generate Bezier
            for ratio in np.arange(0.0, 1.0, step):
                distance = (p1 - p0)
                np0 = p0 + distance * ratio
                distance = (p2 - p1)
                np1 = p1 + distance * ratio
                points.append(np0 + (np1 - np0)*ratio)
            points.append(p2)
                
            collision = False
            for i in range(len(points)-1):
                pygame.draw.line(screen, (0, 0, 0), points[i].get_xy(), points[i+1].get_xy(), 5)
                dv = points[i+1] - points[i]
                dv.normalize()
                dx, dy = dv.get_xy()
    #            print(points[i+1], points[i])
    #            print(-dy, dx)
                print(dy, -dx)
                normal = Vector([dy, -dx])
                
                ac = points[i] - body.position
                ab = points[i] - points[i+1]
                if (ac.cross(ab) / ab.magnitude()) < body.radius:
                    collision = True
                    
    #                Ri - 2 N (Ri . N)
                    body.velocity = body.velocity - normal * (body.velocity * normal) * 2
            
        
            
            
            
         
        
             
    @staticmethod   
    def wall_collision(body):
        x, y = body.position.get_xy()
        if x < 25 + body.radius:
            body.position.set_x(25 + body.radius)
            body.velocity.mul_x(body.wall_restitution)
        elif x > 475 - body.radius:
            body.position.set_x(475 - body.radius)
            body.velocity.mul_x(body.wall_restitution)
        
        if y < 25 + body.radius:
            body.position.set_y(25 + body.radius)
            body.velocity.mul_y(body.wall_restitution)
        elif y > 675 - body.radius:
            body.position.set_y(675 - body.radius)
            body.velocity.mul_y(body.wall_restitution)
            
        
            
        

    @staticmethod
    def inter_body_collision(bodies, dt, restitution=0.9):
        position_0 = bodies[0].position
        position_1 = bodies[1].position
        total_radius = bodies[0].radius + bodies[1].radius
        
        middle = position_0 - position_1
        distance = middle.magnitude()
        
        if distance <= 0.0 or distance >= (total_radius):
            return None
        
        normal = middle * (1.0/distance)
        penetration = total_radius - distance
        
        Contact(bodies, normal, penetration, restitution).resolve(dt)
            
    def update(self, dt, screen):
        for body in self.bodies:
            body.draw(screen)
        
        for body in self.bodies:
            body.clear_accumulators()
            
#        self.aiforce.set_force(self.ai.move())
            
        self.forces.update_forces(dt)
        
        # Move body based 
        for body in self.bodies:
            body.integrate(dt)
            self.corner_collision(body, screen)
            self.wall_collision(body)
            
        for i in range(len(self.bodies)):
            for j in range(i, len(self.bodies)):
                if i == j: continue
                self.inter_body_collision((self.bodies[i], self.bodies[j]), dt)
                
                    
    
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
                
        dt = clock.tick_busy_loop(60)
        
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), (25, 25, 450, 650), 0)
        env.update(dt, screen)
        
        pygame.display.update()
#        done = True
    
    
    pygame.quit ()  