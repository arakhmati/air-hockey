import numpy as np

class Dimensions(object):

    def __init__(self,
                 width=450,
                 height=800,
                 vertical_margin=85,
                 horizontal_margin=20,
                 goalpost_length=160,
                 arc_radius=130,
                 mallet_radius=27,
                 target_radius=55,
                 bezier_ratio=0.3):
        ############ Parameters ############
        self.width = width
        self.height = height

        self.vertical_margin = vertical_margin
        self.horizontal_margin = horizontal_margin

        self.goalpost_length = goalpost_length

        self.arc_radius = arc_radius
        
        self.mallet_radius = mallet_radius
        self.puck_radius = int(self.mallet_radius / 68 * 63)
        self.target_radius = target_radius

        self.bezier_ratio = bezier_ratio

        self.puck_offset_multiplier = 5
        self.mallet_offset_multiplier = 2

        ############ Computed Values ############
        self.table_top    = 0
        self.table_bottom = self.height
        self.table_left   = 0
        self.table_right  = self.width

        self.center = np.array([self.width//2, self.height//2], dtype=np.float32)

        self.rink_top    = self.table_top    + self.vertical_margin
        self.rink_bottom = self.table_bottom - self.vertical_margin
        self.rink_left   = self.table_left   + self.horizontal_margin
        self.rink_right  = self.table_right  - self.horizontal_margin
        self.rink_width  = self.rink_right   - self.rink_left
        self.rink_height = self.rink_bottom  - self.rink_top

        self.center_left  = np.array([self.rink_left,  self.center[1]], dtype=np.float32)
        self.center_right = np.array([self.rink_right, self.center[1]], dtype=np.float32)

        # Anti-clockwise
        self.arc_top_left_start      = np.array([self.rink_left + self.arc_radius, self.rink_top], dtype=np.float32)
        self.arc_top_left_center     = np.array([self.rink_left, self.rink_top], dtype=np.float32)
        self.arc_top_left_end        = np.array([self.rink_left, self.rink_top + self.arc_radius], dtype=np.float32)
        self.arc_bottom_left_start   = np.array([self.rink_left, self.rink_bottom - self.arc_radius], dtype=np.float32)
        self.arc_bottom_left_center  = np.array([self.rink_left, self.rink_bottom], dtype=np.float32)
        self.arc_bottom_left_end     = np.array([self.rink_left + self.arc_radius, self.rink_bottom], dtype=np.float32)
        self.arc_bottom_right_start  = np.array([self.rink_right - self.arc_radius, self.rink_bottom], dtype=np.float32)
        self.arc_bottom_right_center = np.array([self.rink_right, self.rink_bottom], dtype=np.float32)
        self.arc_bottom_right_end    = np.array([self.rink_right, self.rink_bottom - self.arc_radius], dtype=np.float32)
        self.arc_top_right_start     = np.array([self.rink_right, self.rink_top + self.arc_radius], dtype=np.float32)
        self.arc_top_right_center    = np.array([self.rink_right, self.rink_top], dtype=np.float32)
        self.arc_top_right_end       = np.array([self.rink_right - self.arc_radius, self.rink_top], dtype=np.float32)

        self.arc_top_left     = [self.arc_top_left_start, self.arc_top_left_center, self.arc_top_left_end]
        self.arc_top_right    = [self.arc_top_right_start, self.arc_top_right_center, self.arc_top_right_end]
        self.arc_bottom_left  = [self.arc_bottom_left_start, self.arc_bottom_left_center, self.arc_bottom_left_end]
        self.arc_bottom_right = [self.arc_bottom_right_start, self.arc_bottom_right_center, self.arc_bottom_right_end]

        self.half_goalpost_length = goalpost_length//2
        self.post_top_left     = np.array([self.center[0] - self.half_goalpost_length, self.rink_top], dtype=np.float32)
        self.post_top_right    = np.array([self.center[0] + self.half_goalpost_length, self.rink_top], dtype=np.float32)
        self.post_bottom_left  = np.array([self.center[0] - self.half_goalpost_length, self.rink_bottom], dtype=np.float32)
        self.post_bottom_right = np.array([self.center[0] + self.half_goalpost_length, self.rink_bottom], dtype=np.float32)

        self.top_mallet_position    = np.array([self.center[0], self.rink_top    + self.mallet_offset_multiplier * self.mallet_radius], dtype=np.float32)
        self.bottom_mallet_position = np.array([self.center[0], self.rink_bottom - self.mallet_offset_multiplier * self.mallet_radius], dtype=np.float32)

        self.top_goal    = self.rink_top    - self.mallet_radius
        self.bottom_goal = self.rink_bottom + self.mallet_radius

    def random_position(self, obj, top, bottom):
        return np.array([
                np.random.randint(
                        self.rink_left + obj.radius,
                        self.rink_right - obj.radius
                        ),
                np.random.randint(
                        top + obj.radius,
                        bottom - obj.radius
                        )])