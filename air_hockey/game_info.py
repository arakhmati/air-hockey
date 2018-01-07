import numpy as np

class GameInfo(object):
    def __init__(self, frame):
        self.frame = frame
        self.action = np.zeros(2, dtype=np.float32)
        self.adversarial_action = np.zeros(2, dtype=np.float32)
        self.puck_was_hit = False
        self.scored = False
        self.puck_is_at_the_bottom = False
        self.distance_decreased = False

    def set_action(self, action):
        self.action[:] = action

    def set_adversarial_action(self, adversarial_action):
        self.adversarial_action[:] = adversarial_action