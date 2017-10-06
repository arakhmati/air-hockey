import pygame
from air_hockey import AirHockey

if __name__ == "__main__":
    air_hockey = AirHockey()
    while True:
        if any([event.type == pygame.QUIT for event in pygame.event.get()]): break
        air_hockey.step()
    pygame.quit ()
