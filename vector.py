import numpy as np
import numbers

class Vector(object):
    def __init__(self, v=np.zeros(2)):
        self._size = len(v)
        if isinstance(v, list):
            self._v = np.array(v, dtype=np.float)
        if isinstance(v, tuple):
            self._v = np.array(v, dtype=np.float)
        elif isinstance(v, np.ndarray):
            self._v = v
        
    def magnitude(self):
        return np.linalg.norm(self._v)
    
    def squar_magnitude(self):
        return np.sum(np.transpose(self._v) * self._v)
    
    def normalize(self):
        mag = self.magnitude()
        
        if mag != 0.0:
            self._v /= mag
        
    def __add__(self, vector):
        return Vector(self._v + vector._v)
    
    def add(self, vector):
        self._v += vector._v
        
    def __sub__(self, vector):
        return Vector(self._v - vector._v)
    
    def sub(self, vector):
        self._v -= vector._v
        
    def __str__(self):
        return str(self._v[0]) + ' ' + str(self._v[1])
    
            
    def __mul__(self, b):
        if isinstance(b, numbers.Number): # scalar
            return Vector(self._v * b)
        elif isinstance(b, Vector):       # vector -> dot product
            return self._v.dot(b._v)
        else:
            raise ValueError('Vector can only be multipled by another Vector or a scalar' )
    
    def mul(self, scalar):
        self._v *= scalar
        
    def cross(self, vector):
        return np.cross(self._v, vector._v)
        
    def __truediv__(self, scalar):
        if isinstance(scalar, numbers.Number):
            if scalar == 0:
                raise ValueError('Vector cannot be divided by zero')
            else:
                return Vector(self._v / scalar)
        else:
            raise ValueError('Vector can only be divided a scalar' )
        
        
    def clear(self):
        self._v = np.zeros(self._size, dtype=np.float)
        
    def get_xy(self):
        return self._v[0], self._v[1]
    
    def set_x(self, value):
        self._v[0] = value
        
    def set_y(self, value):
        self._v[1] = value

    def mul_x(self, scalar):
        self._v[0] *= scalar
    
    def mul_y(self, scalar):
        self._v[1] *= scalar
        
    def __repr__(self):
        return str(self._v)
        

     
    