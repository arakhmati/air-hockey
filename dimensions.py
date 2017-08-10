############ Adjustable ############
width = 450
height = 800

vertical_margin = 80
horizontal_margin = 15

goalpost_length = 150

arc_radius = 100

body_radius = 20

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

center = [width//2, height//2]

rink_top    = table_top    + vertical_margin
rink_bottom = table_bottom - vertical_margin
rink_left   = table_left   + horizontal_margin
rink_right  = table_right  - horizontal_margin
rink_width = rink_right - rink_left
rink_height = rink_bottom - rink_top

center_left  = [rink_left, center[1]]
center_right = [rink_right, center[1]]

# Anti-clockwise
arc_top_left_start      = [rink_left + arc_radius, rink_top]
arc_top_left_center     = [rink_left, rink_top]
arc_top_left_end        = [rink_left, rink_top + arc_radius]
arc_bottom_left_start   = [rink_left, rink_bottom - arc_radius]
arc_bottom_left_center  = [rink_left, rink_bottom]
arc_bottom_left_end     = [rink_left + arc_radius, rink_bottom]
arc_bottom_right_start  = [rink_right - arc_radius, rink_bottom]
arc_bottom_right_center = [rink_right, rink_bottom]
arc_bottom_right_end    = [rink_right, rink_bottom - arc_radius]
arc_top_right_start     = [rink_right, rink_top + arc_radius]
arc_top_right_center    = [rink_right, rink_top]
arc_top_right_end       = [rink_right - arc_radius, rink_top]

half_goalpost_length = goalpost_length//2
post_top_left     = [center[0] - half_goalpost_length, rink_top]
post_top_right    = [center[0] + half_goalpost_length, rink_top]
post_bottom_left  = [center[0] - half_goalpost_length, rink_bottom]
post_bottom_right = [center[0] + half_goalpost_length, rink_bottom]


puck_default_position_top    = [center[0], center[1] - puck_offset_multiplier * body_radius]
puck_default_position_bottom = [center[0], center[1] + puck_offset_multiplier * body_radius]
top_mallet_position    = [center[0], rink_top +    mallet_offset_multiplier * body_radius]
bottom_mallet_position = [center[0], rink_bottom - mallet_offset_multiplier * body_radius]

top_goal    = rink_top    - body_radius
bottom_goal = rink_bottom + body_radius

post_center_left  = [rink_left + center[0] - half_goalpost_length, center[1]]
post_center_right = [rink_left + center[0] + half_goalpost_length, center[1]]


circle_top_left     = [arc_top_left_center[0]     + rink_circle_offset, arc_top_left_center[1]     + rink_circle_offset]
circle_top_right    = [arc_top_right_center[0]    - rink_circle_offset, arc_top_right_center[1]    + rink_circle_offset]
circle_bottom_left  = [arc_bottom_left_center[0]  + rink_circle_offset, arc_bottom_left_center[1]  - rink_circle_offset]
circle_bottom_right = [arc_bottom_right_center[0] - rink_circle_offset, arc_bottom_right_center[1] - rink_circle_offset]










        
        