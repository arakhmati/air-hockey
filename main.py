import pygame

from Environment import Environment

env = Environment(width=500, height=700, margin=25)


while True:
    pygame.event.get()
    keys = pygame.key.get_pressed()
    print(keys)
    if keys[pygame.K_w]:
        break        

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
     
    env.update() 

pygame.quit ()