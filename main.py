import os
import glob
import pygame
import itertools

from Environment import Environment

project_path = os.environ['GIT_41X']

env = Environment(width=500, height=700, margin=25)

#while True:
#    pygame.event.get()
#    keys = pygame.key.get_pressed()
#    if keys[pygame.K_w]:
#        break  

games = glob.glob(project_path + '/supervised_data/*')  

if len(games) == 0:
    new_game = project_path + ('/supervised_data/game_%06d' % 0)
else:
    games.sort()
    latest_game = games[-1]
    latest_game_index = int(latest_game[-6:])
    new_game = latest_game[:-6] + ('%06d' % (latest_game_index+1))
os.mkdir(new_game)
    
done = False
for i in itertools.count():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
     
    image, x, y, screen = env.update()
    image.save(screen, new_game + '/%08d_%d_%d.jpg' % (i, x, y))
    
    if done:
        break

pygame.quit ()