import os
import glob
import pygame
import itertools

from environment import Environment
import dimensions as D

project_path = '/home/ahmed/Documents/41X'

#while True:
#    pygame.event.get()
#    keys = pygame.key.get_pressed()
#    if keys[pygame.K_w]:
#        break  
if __name__ == "__main__":
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
    
    env = Environment()

    done = False
    for i in itertools.count():
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        if done: break
                
        dt = clock.tick_busy_loop(60)
        x, y = env.step(dt)
        env.draw(screen)
        
        pygame.display.update()

#        pygame.image.save(screen, new_game + '/%08d_%d_%d.jpg' % (i, x, y))
    
    pygame.quit () 