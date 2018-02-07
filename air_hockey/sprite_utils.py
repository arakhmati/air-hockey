# Collection of functions used to manipulate sprites
# TODO: Refactor
import os
import pygame
import numpy as np
from PIL import Image

dir_path = os.path.dirname(os.path.realpath(__file__))

def load_sprites():

    sprites = {}

    # Diversify the data
    def random_sprite_from_dir(dir_name):
        pngs = [name for name in os.listdir(dir_name) if 'png' in name]
        # Randomly select one
        png = pngs[np.random.randint(len(pngs))]
        return pygame.image.load(dir_name + png)

    sprites['table'] = random_sprite_from_dir(dir_path + '/sprites/table/')

    sprites['puck']        = pygame.image.load(dir_path + '/sprites/puck/red.png')
    sprites['puck_top']    = [pygame.image.load(dir_path + '/sprites/puck/top_{}.png'.format(i))    for i in range(7)]
    sprites['puck_bottom'] = [pygame.image.load(dir_path + '/sprites/puck/bottom_{}.png'.format(i)) for i in range(7)]

    sprites['top_mallet']    = pygame.image.load(dir_path + '/sprites/mallet/red_0.png')
    sprites['bottom_mallet'] = pygame.image.load(dir_path + '/sprites/mallet/robot.png')

    dominant_arm = 'left' if np.random.randint(2) else 'right'
    arm_dir = '/sprites/arm/' + dominant_arm + '/'

    sprites['arm'] = pygame.transform.flip(random_sprite_from_dir(dir_path + arm_dir), False, True)
    return sprites, dominant_arm

def blit_puck(game, puck):
    # TODO: Refactor
    # Draw the puck based on its position near the goal
    if game.dim.rink_top + game.dim.puck_radius <= puck[1] <= game.dim.rink_bottom - game.dim.puck_radius:
        game.screen.blit(game.sprites['puck'], puck - game.dim.puck_radius)
    elif game.dim.rink_top - game.dim.puck_radius <= puck[1] <= game.dim.center[1]:
        if game.dim.rink_top + game.dim.puck_radius * 0.7 <= puck[1]:
            game.screen.blit(game.sprites['puck_top'][6], puck - game.dim.puck_radius)
        elif game.dim.rink_top + game.dim.puck_radius * 0.4 <= puck[1]:
            game.screen.blit(game.sprites['puck_top'][5], puck - game.dim.puck_radius)
        elif game.dim.rink_top + game.dim.puck_radius * 0.1 <= puck[1]:
            game.screen.blit(game.sprites['puck_top'][4], puck - game.dim.puck_radius)
        elif game.dim.rink_top - game.dim.puck_radius * 0.1 <= puck[1]:
            game.screen.blit(game.sprites['puck_top'][3], puck - game.dim.puck_radius)
        elif game.dim.rink_top - game.dim.puck_radius * 0.4 <= puck[1]:
            game.screen.blit(game.sprites['puck_top'][2], puck - game.dim.puck_radius)
        elif game.dim.rink_top - game.dim.puck_radius * 0.7 <= puck[1]:
            game.screen.blit(game.sprites['puck_top'][1], puck - game.dim.puck_radius)
        elif game.dim.rink_top - game.dim.puck_radius       <= puck[1]:
            game.screen.blit(game.sprites['puck_top'][0], puck - game.dim.puck_radius)
    elif game.dim.center[1] <= puck[1] <= game.dim.rink_bottom + game.dim.puck_radius:
        if   puck[1] <= game.dim.rink_bottom - game.dim.puck_radius * 0.7:
            game.screen.blit(game.sprites['puck_bottom'][6], puck - game.dim.puck_radius)
        elif puck[1] <= game.dim.rink_bottom - game.dim.puck_radius * 0.4:
            game.screen.blit(game.sprites['puck_bottom'][5], puck - game.dim.puck_radius)
        elif puck[1] <= game.dim.rink_bottom - game.dim.puck_radius * 0.1:
            game.screen.blit(game.sprites['puck_bottom'][4], puck - game.dim.puck_radius)
        elif puck[1] <= game.dim.rink_bottom + game.dim.puck_radius * 0.1:
            game.screen.blit(game.sprites['puck_bottom'][3], puck - game.dim.puck_radius)
        elif puck[1] <= game.dim.rink_bottom + game.dim.puck_radius * 0.4:
            game.screen.blit(game.sprites['puck_bottom'][2], puck - game.dim.puck_radius)
        elif puck[1] <= game.dim.rink_bottom + game.dim.puck_radius * 0.7:
            game.screen.blit(game.sprites['puck_bottom'][1], puck - game.dim.puck_radius)
        elif puck[1] <= game.dim.rink_bottom + game.dim.puck_radius:
            game.screen.blit(game.sprites['puck_bottom'][0], puck - game.dim.puck_radius)

def generate_puck_sprites():
    ''' Utility function to generate sprites that will simulate the puck going inside the goal area '''

    image = Image.open('sprites/puck.png')
    image = image.convert('RGBA')
    original_data = np.array(image)

    step = 0.125
    for ratio in np.arange(step, 1.0, step):
        data = np.copy(original_data)
        data[int(ratio*50):50, :, :] = [255, 255, 255, 0]
        image = Image.fromarray(data)
        image.save('sprites/puck/bottom_{}.png'.format(int(ratio*8-1)))
        data = data[::-1, :, :]
        image = Image.fromarray(data)
        image.save('sprites/puck/top_{}.png'.format(int(ratio*8-1)))
