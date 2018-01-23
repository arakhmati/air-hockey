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
            intersects = self.intersects((puck_px, puck_py), (puck_vx, puck_vy), [self.dim.post_top_left, self.dim.post_top_right])
            if intersects is not None:
                goal_px, goal_py = intersects[0]
            else:
                goal_px, goal_py = (self.dim.center[0], self.dim.rink_top)
        elif self.mode == 'bottom':
            intersects = self.intersects((puck_px, puck_py), (puck_vx, puck_vy), [self.dim.post_bottom_left, self.dim.post_bottom_right])
            if intersects is not None:
                goal_px, goal_py = intersects[0]
            else:
                goal_px, goal_py = (self.dim.center[0], self.dim.rink_bottom)

        if self.mode is 'top':
            reachable = self.dim.rink_top <= puck_py <=  self.dim.center[1]
        elif self.mode == 'bottom':
            reachable = self.dim.center[1] <= puck_py <=  self.dim.rink_bottom

        x, y = 0, 0
        if not reachable:
            x, y = 0, 0
#            x = np.random.randint(-1, 2)
#            y = np.random.randint(-1, 2)
#            if   x == -1 and px < self.dim.rink_left  + self.mallet.radius + self.dim.goalpost_length//2: x =  1
#            elif x ==  1 and px > self.dim.rink_right - self.mallet.radius - self.dim.goalpost_length//2: x = -1
#            if self.mode is 'top':
#                if y == 1 and py > (self.dim.center[1] - self.dim.goalpost_length): y = -1
#            elif self.mode == 'bottom':
#                if y == -1 and py < (self.dim.center[1] + self.dim.goalpost_length): y = 1
#            print('{:15} {:4d} {:4d}'.format('not reachable', x, y))

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