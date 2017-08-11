import numpy as np
import dimensions as D

class Score(object):
    puck_default_top_position    = np.array(D.puck_default_top_position, dtype=np.float32)
    puck_default_bottom_position = np.array(D.puck_default_bottom_position, dtype=np.float32)
    
    def __init__(self):
        self._score = {'top': 0, 'bottom': 0}
        
    def update(self, puck):
        _, y = puck.position
        
        scored = True
        if y < D.top_goal:
            self._score['bottom'] += 1
            np.copyto(puck.default_position, Score.puck_default_bottom_position)
        elif y > D.bottom_goal:
            self._score['top'] += 1
            np.copyto(puck.default_position, Score.puck_default_top_position)
        else:
            scored = False
        return scored
            
    def __repr__(self):
        return str(self._score)