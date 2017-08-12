from abc import ABC, abstractmethod
import numpy as np
import random

import vector as V
import dimensions as D
import physical_constants as P

class AI(ABC):
    @abstractmethod
    def move(self):
        pass

class RuleBasedAI(AI):
    def move(self):
        pass
    
class MachineLearningAI(AI):
    def __init__(self, mallet, puck, mode):
        self.mallet = mallet
        self.puck = puck
        self.mode = mode
        self.force = np.zeros(2, dtype=np.float32)
        
    def intersects(self, origin, direction, line):
        origin = np.array(origin, dtype=np.float32)
        direction = np.array(direction, dtype=np.float32)
        v1 = origin - line[0]
        v2 = line[1] - line[0]
        v3 = np.array([-direction[1], direction[0]], dtype=np.float32)
        v2_d_v3 = np.dot(v2, v3)
        if v2_d_v3 != 0:
            t1 = np.cross(v2, v1) / v2_d_v3
            t2 = np.dot(v1, v3)   / v2_d_v3
        else:
            t1 = t2 = -1
        if t1 >= 0.0 and t2 >= 0.0 and t2 <= 1.0:
            return [origin + t1 * direction]
        return None
    
    def move(self):
                
        px, py = self.mallet.position
        vx, vy = self.mallet.get_velocity()
        
        puck = self.puck
        puck_px, puck_py = self.puck.position
        puck_vx, puck_vy = self.puck.get_velocity()
            
            
        if self.mode is 'top':
            
            intersects = self.intersects((puck_px, puck_py), (puck_vx, puck_vy), [D.post_top_left, D.post_top_right])
            if intersects != None:
                goal_px, goal_py = intersects[0]
            else:
                goal_px, goal_py = (D.center[0], D.rink_top)
            
            x, y = 0, 0
            reachable = D.rink_top <= puck_py <=  D.center[1]
            if not reachable:
                x = random.randrange(-1, 2, 1)
                y = random.randrange(-1, 2, 1)
                
                if x == -1 and px < D.rink_left  + self.mallet.radius + D.goalpost_length//2: x = 1
                elif x == 1 and px > D.rink_right - self.mallet.radius - D.goalpost_length//2: x = -1
                if y == 1 and py > (D.center[1] - D.goalpost_length): y = -1
                
            else:
                if puck_vy > 0:
                    if puck_px < px:
                        x = -1
                    if puck_px > px:
                        x = 1
                    if puck_py < py:
                        y = -1
                    if puck_py > py:
                        y = 1
                else:
                    too_fast = V.magnitude(puck.get_velocity()) > 0.8*P.puck_maximum_speed 
                    
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
                            
            self.force[:] = x*8, y*10
    
        elif self.mode == 'bottom':
            intersects = self.intersects((puck_px, puck_py), (puck_vx, puck_vy), [D.post_bottom_left, D.post_bottom_right])
            if intersects != None:
                goal_px, goal_py = intersects[0]
            else:
                goal_px, goal_py = (D.center[0], D.rink_bottom)
            
            x, y = 0, 0
            reachable = D.center[1] <= puck_py <=  D.rink_bottom
            if not reachable:
                x = random.randrange(-1, 2, 1)
                y = random.randrange(-1, 2, 1)
                
                if x == -1 and px < D.rink_left  + self.mallet.radius + D.goalpost_length//2: x = 1
                elif x == 1 and px > D.rink_right - self.mallet.radius - D.goalpost_length//2: x = -1
                if y == -1 and py < (D.center[1] + D.goalpost_length): y = 1
                
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
                    too_fast = V.magnitude(puck.get_velocity()) > 0.8*P.puck_maximum_speed 
                    
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
                        
            self.force[:] = x*8, y*10