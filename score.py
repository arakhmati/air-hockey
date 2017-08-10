from vector import Vector
import dimensions as D

class Score(object):
    def __init__(self):
        self._score = {'top': 0, 'bottom': 0}
        
    def update(self, puck):
        _, y = puck.position.get_xy()
        
        scored = True
        if y < D.top_goal:
            self._score['bottom'] += 1
            puck.default_position = Vector(D.puck_default_position_bottom)
        elif y > D.bottom_goal:
            self._score['top'] += 1
            puck.default_position = Vector(D.puck_default_position_top)
        else:
            scored = False
            
        return scored
            