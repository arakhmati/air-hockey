import numpy as np

class GameInfo(object):
    def __init__(self,
                 frame,
                 action=None,
                 adversarial_action=None,
                 scored=None,
                 puck_was_hit=False,
                 puck_is_at_the_bottom=False,
                 distance_decreased=False,
                 hit_the_border=False):
        
        self.frame = np.copy(frame)
        
        if action is None:
            self.action = np.zeros(2, dtype=np.float32)
        else:
            self.action = np.copy(action)
            
        if adversarial_action is None:
            self.adversarial_action = np.zeros(2, dtype=np.float32)
        else:
            self.adversarial_action = np.copy(adversarial_action)
            
        self.puck_was_hit = puck_was_hit
        self.scored = scored
        self.puck_is_at_the_bottom = puck_is_at_the_bottom
        self.distance_decreased = distance_decreased
        self.hit_the_border = hit_the_border