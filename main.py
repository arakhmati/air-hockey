import os
import glob
import time
import pygame
import itertools
import numpy as np
import scipy.misc
import matplotlib.pyplot as plt

from environment import Environment
import dimensions as D

project_path = '/home/ahmed/Documents/41X'

#while True:
#    pygame.event.get()
#    keys = pygame.key.get_pressed()
#    if keys[pygame.K_w]:
#        break  

if __name__ == "__main__":
#def main():
#    games = glob.glob(project_path + '/supervised_data/*')
#    games = list(filter(lambda x: 'npz' not in x, games))
#    
#    if len(games) == 0:
#        new_game = project_path + ('/supervised_data/game_%06d' % 0)
#    else:
#        games.sort()
#        latest_game = games[-1]
#        latest_game_index = int(latest_game[-6:])
#        new_game = latest_game[:-6] + ('%06d' % (latest_game_index+1))
#    os.mkdir(new_game)
    
    pygame.init()
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((D.width, D.height))
    
#    screen = pygame.Surface((D.width, D.height)) 
    
    env = Environment()
    
#    data = np.zeros((100, 450, 800, 3), dtype=np.uint8)

    done = False
    for i in itertools.count():
#        if i == 3600:
#            break
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        if done: break
        dt = clock.tick_busy_loop(60)
        tic = time.time()
        x, y = env.step(dt)
        env.draw(screen)
        
#        data[i] = pygame.surfarray.array3d(screen)
        
        pygame.display.update()
        toc = time.time()
        print(toc-tic)
#        pygame.image.save(surface, new_game + '/%08d_%d_%d.jpg' % (i, x, y))
#        import matplotlib.pyplot as plt
#        array = pygame.surfarray.array3d(screen)
#        plt.imshow(array)
#        plt.show()
        
    pygame.quit ()
    
#    print('saving data')
#    for i in range(len(data)):
#        scipy.misc.imsave('%04d.jpg' % i, data[i])
#    
#import cProfile as profile
#profile.run('main()')