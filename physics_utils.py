import math


def distance(a, b):
    return math.sqrt( (b[0]-a[0])**2 + (b[1]-a[1])**2 )        

def angle(a, b):
    return norm_angle((math.atan2(b[1]-a[1],b[0]-a[0])*180)/math.pi)

def distance_from_O(a):
    return distance((0,0),a)        

def angle_from_O(a):
    return angle((0,0),a)    

def norm_angle(a):
    return (a+360) % 360