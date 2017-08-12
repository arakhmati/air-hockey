import numpy as np

############ Adjustable ############
width = 450
height = 800

vertical_margin = 85
horizontal_margin = 20

goalpost_length = 160

arc_radius = 130

mallet_radius = 27
puck_radius = int(mallet_radius / 68 * 63)

bezier_ratio = 0.1

puck_offset_multiplier = 5
mallet_offset_multiplier = 2

rink_circle_offset = 75
rink_circle_radius = 40

############ Computed ############
table_top    = 0
table_bottom = height
table_left   = 0
table_right  = width

center = np.array([width//2, height//2], dtype=np.float32)

rink_top    = table_top    + vertical_margin
rink_bottom = table_bottom - vertical_margin
rink_left   = table_left   + horizontal_margin
rink_right  = table_right  - horizontal_margin
rink_width = rink_right - rink_left
rink_height = rink_bottom - rink_top

center_left  = np.array([rink_left, center[1]], dtype=np.float32)
center_right = np.array([rink_right, center[1]], dtype=np.float32)

# Anti-clockwise
arc_top_left_start      = np.array([rink_left + arc_radius, rink_top], dtype=np.float32)
arc_top_left_center     = np.array([rink_left, rink_top], dtype=np.float32)
arc_top_left_end        = np.array([rink_left, rink_top + arc_radius], dtype=np.float32)
arc_bottom_left_start   = np.array([rink_left, rink_bottom - arc_radius], dtype=np.float32)
arc_bottom_left_center  = np.array([rink_left, rink_bottom], dtype=np.float32)
arc_bottom_left_end     = np.array([rink_left + arc_radius, rink_bottom], dtype=np.float32)
arc_bottom_right_start  = np.array([rink_right - arc_radius, rink_bottom], dtype=np.float32)
arc_bottom_right_center = np.array([rink_right, rink_bottom], dtype=np.float32)
arc_bottom_right_end    = np.array([rink_right, rink_bottom - arc_radius], dtype=np.float32)
arc_top_right_start     = np.array([rink_right, rink_top + arc_radius], dtype=np.float32)
arc_top_right_center    = np.array([rink_right, rink_top], dtype=np.float32)
arc_top_right_end       = np.array([rink_right - arc_radius, rink_top], dtype=np.float32)

half_goalpost_length = goalpost_length//2
post_top_left     = np.array([center[0] - half_goalpost_length, rink_top], dtype=np.float32)
post_top_right    = np.array([center[0] + half_goalpost_length, rink_top], dtype=np.float32)
post_bottom_left  = np.array([center[0] - half_goalpost_length, rink_bottom], dtype=np.float32)
post_bottom_right = np.array([center[0] + half_goalpost_length, rink_bottom], dtype=np.float32)

puck_default_top_position    = np.array([center[0], center[1] - puck_offset_multiplier * puck_radius], dtype=np.float32)
puck_default_bottom_position = np.array([center[0], center[1] + puck_offset_multiplier * puck_radius], dtype=np.float32)
top_mallet_position    = np.array([center[0], rink_top +    mallet_offset_multiplier * mallet_radius], dtype=np.float32)
bottom_mallet_position = np.array([center[0], rink_bottom - mallet_offset_multiplier * mallet_radius], dtype=np.float32)

top_goal    = rink_top    - mallet_radius
bottom_goal = rink_bottom + mallet_radius

post_center_left  = np.array([rink_left + center[0] - half_goalpost_length, center[1]], dtype=np.float32)
post_center_right = np.array([rink_left + center[0] + half_goalpost_length, center[1]], dtype=np.float32)

circle_top_left     = np.array([arc_top_left_center[0]     + rink_circle_offset, arc_top_left_center[1]     + rink_circle_offset], dtype=np.float32)
circle_top_right    = np.array([arc_top_right_center[0]    - rink_circle_offset, arc_top_right_center[1]    + rink_circle_offset], dtype=np.float32)
circle_bottom_left  = np.array([arc_bottom_left_center[0]  + rink_circle_offset, arc_bottom_left_center[1]  - rink_circle_offset], dtype=np.float32)
circle_bottom_right = np.array([arc_bottom_right_center[0] - rink_circle_offset, arc_bottom_right_center[1] - rink_circle_offset], dtype=np.float32)










        
        