import pygame

from circle import Disc, Mallet
from force import ForceRegistry, RandomForce, KeyboardForce
from contact import Contact
          
class World(object):
    def __init__(self):
        self.bodies = [Disc([250, 350], 25), Disc([375, 375], 25), Disc([375, 125], 25), Mallet([250, 125], 25, color=(0, 255, 0)), Mallet([250, 575], 25), Mallet([125, 575], 25), Mallet([125, 125], 25)]
        
        self.forces = ForceRegistry()
        self.forces.add(self.bodies[3], KeyboardForce())
        for body in self.bodies[4:]:
            self.forces.add(body, RandomForce())

    @staticmethod
    def detect_collision(circle_1, circle_2, restitution=0.9):
        position_1 = circle_1.get_position()
        position_2 = circle_2.get_position()
        
        middle = position_1 - position_2
        distance = middle.magnitude()
        
        if distance <= 0.0 or distance >= (circle_1.radius + circle_2.radius):
            return None
        
        normal = middle * (1.0/distance)
        penetration = circle_1.radius + circle_2.radius - distance
        
        contact = Contact((circle_1, circle_2), normal, penetration, restitution)
        return contact
            
    def update(self, dt, screen):
        for body in self.bodies:
            body.draw(screen)
        
        for body in self.bodies:
            body.clear_accumulators()
            
        self.forces.update_forces(dt)
        
        for body in self.bodies:
            body.integrate(dt)
            
        for i in range(len(self.bodies)):
            for j in range(i, len(self.bodies)):
                if i == j: continue
                contact = self.detect_collision(self.bodies[i], self.bodies[j])
                if contact != None:
                    contact.resolve(dt)
                    
    
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
    
    
    pygame.quit ()  