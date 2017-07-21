import pygame

from Environment import Environment

env = Environment(width=500, height=700, margin=25)
  
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    env.update()  

pygame.quit ()