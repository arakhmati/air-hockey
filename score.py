from vector import Vector

class Score(object):
    def __init__(self):
        self._score = {'top': 0, 'bottom': 0}
        
    def update(self, puck):
        _, y = puck.position.get_xy()
        
        scored = True
        if y < 20:
            self._score['bottom'] += 1
            puck.default_position = Vector([250, 400])
        elif y > 680:
            self._score['top'] += 1
            puck.default_position = Vector([250, 300])
        else:
            scored = False
            
        return scored
            