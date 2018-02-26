import numpy as np
import air_hockey.vector as V
import air_hockey.phy_const as P

class AI(object):
    def __init__(self, mallet, puck, mode, dim):
        self.mallet = mallet
        self.puck = puck
        self.mode = mode
        self.dim = dim
        self._force = np.zeros(2, dtype=np.float32)

    def move(self):

        px, py = self.mallet.position
        vx, vy = self.mallet.get_velocity()

        puck = self.puck
        puck_px, puck_py = self.puck.position
        puck_vx, puck_vy = self.puck.get_velocity()

        if self.mode is 'top':
            goal_px, goal_py = (self.dim.center[0], self.dim.rink_top + 55)
        elif self.mode == 'bottom':
            goal_px, goal_py = (self.dim.center[0], self.dim.rink_bottom - 55)

        if self.mode is 'top':
            reachable = self.dim.rink_top <= puck_py <=  self.dim.center[1]
        elif self.mode == 'bottom':
            reachable = self.dim.center[1] <= puck_py <=  self.dim.rink_bottom

        x, y = 0, 0
        if not reachable:
            if self.mode is 'top':
                target_px, target_py = (self.dim.center[0], self.dim.rink_top + 80)
            elif self.mode == 'bottom':
                target_px, target_py = (self.dim.center[0], self.dim.rink_bottom - 80)
            def defend_goal(goal, p):
                diff = goal - p
                if abs(diff) < 40: return  0
                elif diff > 0:    return  1
                else:             return -1
            x = defend_goal(target_px, px)
            y = defend_goal(target_py, py)
            # print('{:15} {:4d} {:4d}'.format('not reachable', x, y))

        else:
            if puck_vy <= 0:
                if puck_px < px: x = -1
                if puck_px > px: x = 1
                if puck_py < py: y = -1
                if puck_py > py: y = 1
#                print('{:15} {:4d} {:4d}'.format('stationary', x, y))
            else:
                too_fast = V.magnitude(puck.get_velocity()) > 0.8*P.puck_maximum_speed
                if too_fast:
                    def save_goal(goal, p):
                        diff = goal - p
                        if abs(diff) < 5: return  0
                        elif diff > 0:    return  1
                        else:             return -1
                    x = save_goal(goal_px, px)
                    y = save_goal(goal_py, py)
#                    print('{:15} {:4d} {:4d}'.format('too fast', x, y))
                else:
                    if puck_px < px: x = -1
                    if puck_px > px: x = 1
                    if puck_py < py: y = -1
                    if puck_py > py: y = 1
#                    print('{:15} {:4d} {:4d}'.format('slow', x, y))

        self._force[:] = x, y
        return self._force