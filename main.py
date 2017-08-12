import os
import cv2
import glob
import pygame
import itertools
import numpy as np
import progressbar

from environment import Environment
import dimensions as D

project_path = os.path.dirname(os.path.realpath(__file__)).replace('air_hockey', '')

if __name__ == "__main__":
    screen_mode = 2
    number_of_frames = 2000
    
    pygame.init()
    if not screen_mode:
        screen = None
        data = np.zeros((number_of_frames, 4, 2), dtype=np.float32)
        bar = progressbar.ProgressBar(max_value=number_of_frames)
    elif screen_mode:
        screen = pygame.display.set_mode((D.width, D.height))
        number_of_frames = -1
    
    env = Environment()

    done = False
    for i in itertools.count():
        if i == number_of_frames: break
        if any([event.type == pygame.QUIT for event in pygame.event.get()]): break
        observations = env.step()
        if screen is None: 
            data[i] = observations
            bar.update(i)
        if screen is not None: 
            env.render(screen)
            pygame.display.update()
    
    if screen is None:
        if os.path.isfile('game.avi'): os.remove('game.avi')
        writer = cv2.VideoWriter('game.avi', cv2.VideoWriter_fourcc(*'PIM1'), 60, (D.width, D.height-2*D.vertical_margin))
        screen = pygame.Surface((D.width, D.height)) 
        bar.init()
        for i, observations in enumerate(data):
            env.render_observations(screen, observations)
            x = pygame.surfarray.array3d(screen).astype(np.uint8)
            x = x[:, :, ::-1] # Flip from BGR to RGB
            x = x.transpose((1,0,2)) # Transpose to make it portrait
            x = x[D.vertical_margin:, :, :]
            x = x[:-D.vertical_margin, :, :]
            writer.write(x)
            bar.update(i)
        
    pygame.quit ()