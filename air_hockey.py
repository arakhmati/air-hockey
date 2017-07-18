# sumloky
# (Edward) Sum Lok Yu
#--------------------

# Import a library of functions called 'pygame'
import pygame

from draw_utils import colors, width, height
from draw_utils import draw_rink

from game_utils import Puck, Mallet, Goal, collide, Environment
  

env = Environment(width, height)

score = {'cpuScore': 0, 'playerScore': 0}

size=[width, height]
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Air Hockey")
  
clock=pygame.time.Clock()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    (mouseX, mouseY) = pygame.mouse.get_pos()
    env.update(mouseX, mouseY)  
               
    screen.fill(colors['black'])
    draw_rink(screen)
    for drawable in env.get_drawables():
        drawable.draw(screen)
    pygame.display.flip()
    
    clock.tick(60)  

pygame.quit ()
