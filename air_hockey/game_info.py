import numpy as np

class GameInfo(object):
    def __init__(self,
                 frame,
                 robot_action=None,
                 human_action=None,
                 scored=None,
                 puck_was_hit=False,
                 puck_is_at_the_bottom=False,
                 distance_decreased=False,
                 hit_the_border=False,
                 in_the_target=False):
        
        self.frame = np.copy(frame)
        
        if robot_action is None:
            self.robot_action = np.zeros(2, dtype=np.float32)
        else:
            self.robot_action = np.copy(robot_action)
            
        if human_action is None:
            self.human_action = np.zeros(2, dtype=np.float32)
        else:
            self.human_action = np.copy(human_action)
            
        self.puck_was_hit = puck_was_hit
        self.scored = scored
        self.puck_is_at_the_bottom = puck_is_at_the_bottom
        self.distance_decreased = distance_decreased
        self.hit_the_border = hit_the_border
        self.in_the_target = in_the_target