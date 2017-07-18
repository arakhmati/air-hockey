import math
from physics_utils import angle_from_O, distance_from_O, angle, distance, norm_angle

class Vector:

    def __init__( self, angle, magnitude):
        self.__angle = (angle+360)%360 
        self.__magnitude = magnitude
        
    def get_angle(self):
        return self.__angle

    def get_magnitude(self):
        return self.__magnitude
        
    def set_angle(self,angle):
        self.__angle = (angle+360)%360 
    def set_magnitude(self,magnitude):
        self.__magnitude = magnitude
        
    def get_xy(self):
        return math.cos(self.get_angle()*math.pi/180.0)*self.get_magnitude(),math.sin(self.get_angle()*math.pi/180.0)*self.get_magnitude()

    def set_xy(self,a):
        angle = angle_from_O(a)
        magnitude = distance_from_O(a)
        self.set_angle(angle)
        self.set_magnitude(magnitude)   

    def __add__(self,v):
        s1 = self.get_xy()
        s2 = v.get_xy()
        s3 = [s1[0]+s2[0],s1[1]+s2[1]]
        return Vector(angle( (0,0), s3),distance( (0,0), s3))

    def __sub__(self,v):
        s1 = self.get_xy()
        s2 = v.get_xy()
        s3 = [s1[0]-s2[0],s1[1]-s2[1]]
        return Vector(angle( (0,0), s3),distance( (0,0), s3))
        
    def __mul__( self, v):
        return self.get_magnitude()*v.get_magnitude()*math.cos(norm_angle(self.get_angle()-v.get_angle())*math.pi/180.0)
        
    def __rmul__( self, dt):
        return Vector(self.get_angle(),self.get_magnitude()*dt)
        
    def copy( self):
        return Vector(self.get_angle(),self.get_magnitude())
        
    def normalize( self):
        if self.get_magnitude()>0:
            self.set_magnitude(1)
