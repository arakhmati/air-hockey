import math

from Vector import Vector
from physics_utils import angle_from_O, distance_from_O, distance

class MovingCircle:

    def __init__(self, pos, rink, radius, mass, max_speed, friction):
        self.__pos = Vector(angle_from_O(pos), distance_from_O(pos))
        self.__start_pos_xy = pos
        self.__width, self.__height = 0, 0
        self.__radius = radius
        self.__speed = Vector(0, 0)
        self.__mass = mass
        self.__max_speed = max_speed
        self.__friction = friction
        self.__rink = rink
        
    def get_pos(self):
        return self.__pos

    def get_pos_angle(self):
        return self.get_pos().get_angle()

    def get_pos_magnitude(self):
        return self.get_pos().get_magnitude()

    def get_pos_xy(self):
        return self.get_pos().get_xy()

    def get_radius(self):
        return self.__radius

    def get_speed(self):
        return self.__speed

    def get_speed_angle(self):
        return self.get_speed().get_angle()

    def get_speed_magnitude(self):
        return self.get_speed().get_magnitude()

    def get_speed_xy(self):
        return self.get_speed().get_xy()

    def get_mass(self):
        return self.__mass

    def get_max_speed(self):
        return self.__max_speed
    
    def get_friction(self):
        return self.__friction
    
    def get_rink(self):
        return self.__rink

    def set_pos(self,pos):
        self.__pos = pos

    def set_pos_angle(self,angle):
        self.get_pos().set_angle(angle)

    def set_pos_magnitude(self,magnitude):
        self.get_pos().set_magnitude(magnitude)

    def set_pos_xy(self,pos):
        self.get_pos().set_xy(pos)

    def set_radius(self,radius):
        self.__radius = radius

    def set_speed(self, speed):
        self.__speed = speed

    def set_speed_angle(self,angle):
        self.get_speed().set_angle(angle)

    def set_speed_magnitude(self,magnitude):
        self.get_speed().set_magnitude(magnitude)

    def set_speed_xy(self,speed):
        self.get_speed().set_xy(speed)

    def set_mass(self,m):
        self.__mass = m

    def set_max_speed(self,max_speed):
        self.__max_speed = max_speed 
        
    def get_start_pos_xy(self):
        return self.__start_pos_xy
    
    def set_friction(self,friction):
        self.__friction = friction
        
    def reset(self):
        pos = self.get_start_pos_xy()
        pos_angle = angle_from_O(pos)
        pos_magnitude = distance_from_O(pos)
        self.__pos = Vector(pos_angle,pos_magnitude)
        self.set_speed(Vector(0,0))        
                
    def friction( self, dt):
        if self.get_speed_magnitude()>0:
            self.set_speed_magnitude(self.get_speed_magnitude()-self.get_friction()*dt)
        if self.get_speed_magnitude()<0:
            self.set_speed_magnitude(0)
          
    def collision(self, B, dt):


        dist = distance(self.get_pos_xy(), B.get_pos_xy())
        sumRadii = self.get_radius() + B.get_radius()
        
        if dist > sumRadii:
            return False
        
        dist -= sumRadii
        S = self.get_speed()-B.get_speed()

        if S.get_magnitude()*dt < dist:
            return False

        N = S.copy()
        N.normalize()
        C = B.get_pos()-self.get_pos()
        D = N*C

        if D <= 0:
            return False

        F = C.get_magnitude()**2-D**2

        sumRadiiSquared = sumRadii**2

        if F >= sumRadiiSquared :
            return False

        T = sumRadiiSquared - F

        if T < 0:
            return False

        dist = D - math.sqrt(T)

        if S.get_magnitude()*dt < dist:
            return False

        # Collision happened
        N = B.get_pos()-self.get_pos()
        N.normalize()

        a1 = self.get_speed()*N
        a2 = B.get_speed()*N

        P = (2*(a1-a2))/(self.get_mass()+B.get_mass())
        newA = self.get_speed() - P*B.get_mass()*N
        
        self.set_speed(newA)
        
        if self.get_speed_magnitude()>self.get_max_speed():
            self.set_speed_magnitude(self.get_max_speed())
        
        return True

