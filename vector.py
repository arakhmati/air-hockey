import numpy as np
import numbers

class Vector(object):
    def __init__(self, v=np.zeros(2)):
        self.n = len(v)
        if isinstance(v, list):
            self.v = np.array(v, dtype=np.float)
        elif isinstance(v, np.ndarray):
            self.v = v
        
    def magnitude(self):
        return np.linalg.norm(self.v)
    
    def squar_magnitude(self):
        return np.sum(np.transpose(self.v) * self.v)
    
    def normalize(self):
        mag = self.magnitude()
        
        if mag != 0.0:
            self.v /= mag
        
    def __add__(self, vector):
        return Vector(self.v + vector.v)
    
    def add(self, vector):
        self.v += vector.v
        
    def __sub__(self, vector):
        return Vector(self.v - vector.v)
    
    def sub(self, vector):
        self.v -= vector.v
        
    def __str__(self):
        return str(self.v[0]) + ' ' + str(self.v[1])
    
            
    def __mul__(self, b):
        if isinstance(b, numbers.Number): # scalar
            return Vector(self.v * b)
        elif isinstance(b, Vector):       # vector -> dot product
            return self.v.dot(b.v)
        else:
            raise ValueError('Vector can only be multipled by another Vector or a scalar' )
    
    def mul(self, scalar):
        self.v *= scalar
        
    def __truediv__(self, scalar):
        if isinstance(scalar, numbers.Number):
            if scalar == 0:
                raise ValueError('Vector cannot be divided by zero')
            else:
                return Vector(self.v / scalar)
        else:
            raise ValueError('Vector can only be divided a scalar' )
        
        
    def clear(self):
        self.v = np.zeros(self.n, dtype=np.float)
        

     
    