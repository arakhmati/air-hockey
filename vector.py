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
    
    def normalize(self):
        mag = self.magnitude()
        if mag != 0.0:
            self._v /= mag
        return Vector(self._v)
        
    def __add__(self, vector):
        return Vector(self._v + vector._v)

        
    def __sub__(self, vector):
        return Vector(self._v - vector._v)    
            
    def __mul__(self, b):
        if isinstance(b, numbers.Number): # scalar
            return Vector(self._v * b)
        elif isinstance(b, Vector):       # vector -> dot product
            return self._v.dot(b._v)
        else:
            raise ValueError('Vector can only be multipled by another Vector or a scalar' )
        
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
        
    def __str__(self):
        return str(self._v)
        
    def __repr__(self):
        return str(self._v)
        

     
    