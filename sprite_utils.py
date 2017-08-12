import numpy as np
from PIL import Image
def generate_puck_sprites():

    image = Image.open('sprites/puck.png')
    image = image.convert('RGBA')
    original_data = np.array(image)
    
    step = 0.125
    for ratio in np.arange(step, 1.0, step):
        data = np.copy(original_data)
        data[int(ratio*50):50, :, :] = [255, 255, 255, 0]
        image = Image.fromarray(data)
        image.save('sprites/puck_bottom_{}.png'.format(int(ratio*8-1)))
        data = data[::-1, :, :]
        image = Image.fromarray(data)
        image.save('sprites/puck_top_{}.png'.format(int(ratio*8-1)))