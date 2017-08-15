import numpy as np

class Score(object):
    
    def __init__(self, dim):
        self._score = {'top': 0, 'bottom': 0}
        self.dim = dim
        
    def update(self, puck):
        _, y = puck.position
        
        scored = True
        if y < self.dim.top_goal:
            self._score['bottom'] += 1
            np.copyto(puck.default_position, self.dim.puck_default_bottom_position)
        elif y > self.dim.bottom_goal:
            self._score['top'] += 1
            np.copyto(puck.default_position, self.dim.puck_default_top_position)
        else:
            scored = False
        return scored
            
    def __repr__(self):
        return str(self._score)