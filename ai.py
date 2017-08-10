from abc import ABC
import numpy as np
import random

from vector import Vector
import dimensions as D
import physical_constants as P

class AI(ABC):
    pass

class RuleBasedAI(AI):
    pass
    
class MachineLearningAI(AI):
    def __init__(self, mallet, puck):
        self.mallet = mallet
        self.puck = puck
        
    def intersects(self, origin, direction, line):
        v1 = origin - line[0]
        v2 = line[1] - line[0]
        v3 = np.array([-direction[1], direction[0]])
        t1 = np.cross(v2, v1) / np.dot(v2, v3)
        t2 = np.dot(v1, v3) / np.dot(v2, v3)
        if t1 >= 0.0 and t2 >= 0.0 and t2 <= 1.0:
            return [origin + t1 * direction]
        return None
    
    def move(self):
            
        px, py = self.mallet.position.get_xy()
        vx, vy = self.mallet.get_velocity().get_xy()
        
        puck = self.puck
        puck_px, puck_py = self.puck.position.get_xy()
        puck_vx, puck_vy = self.puck.get_velocity().get_xy()
        
#        intersects = self.intersects(np.array((puck_px, puck_py)), np.array((puck_vx, puck_vy)), goal_line)
#        if intersects != None:
#            goal_px, goal_py = intersects[0]
#        else:
        goal_px, goal_py = (D.center[0], D.rink_top)
        
        x, y = 0, 0
        reachable = D.rink_top <= puck_py <=  D.center[1]
        if not reachable:
            x = random.randrange(-1, 2, 1)
            y = random.randrange(-1, 2, 1)
            
            if x == -1 and px < D.rink_left  + self.mallet.radius + 100*2: x = 1
            elif x == 1 and px > D.rink_right - self.mallet.radius - 100*2: x = -1
            if y == 1 and py > (D.center[1] - D.goalpost_length): y = -1
            
        else:
            if puck_vy < 0:
                if puck_px < px:
                    x = -1
                if puck_px > px:
                    x = 1
                if puck_py < py:
                    y = -1
                if puck_py > py:
                    y = 1
            else:
                too_fast = puck.get_velocity().magnitude() > 0.8*P.maximum_speed 
                
                if too_fast:
                    diff_px = goal_px - px
                    if abs(diff_px) < 5: x = 0
                    elif diff_px > 0:    x = 1
                    else:                x = -1
                    x *= min(abs(diff_px)/20, 1)
                
                    diff_py = goal_py - py
                    if abs(diff_py) < 5: y = 0
                    elif diff_py > 0:    y = 1
                    else:                y = -1
                    y *= min(abs(diff_py)/20, 1)
                else:
                    if puck_px < px:
                        x = -1
                    if puck_px > px:
                        x = 1
                    if puck_py < py:
                        y = -1
                    if puck_py > py:
                        y = 1
                        
        return Vector([x, y])