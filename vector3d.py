from math import sqrt
from numbers import Number


class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, o):
        if isinstance(o, Vector3D):
            return Vector3D(self.x + o.x, self.y + o.y, self.z + o.z)
        if isinstance(o, Number):
            return Vector3D(self.x + o, self.y + o, self.z + o)
        raise TypeError

    def __radd__(self, o):
        return self + o
    
    def __sub__(self, o):
        if isinstance(o, Vector3D):
            return Vector3D(self.x - o.x, self.y - o.y, self.z - o.z)
        if isinstance(o, Number):
            return Vector3D(self.x - o, self.y - o, self.z - o)
        raise TypeError
    
    def __rsub__(self, o):
        if isinstance(o, Vector3D):
            return Vector3D(o.x - self.x, o.y - self.y, o.z - self.z)
        raise TypeError

    def __mul__(self, o):
        if isinstance(o, Number):
            return Vector3D(self.x * o, self.y * o, self.z * o)
        raise TypeError
    
    def __rmul__(self, o):
        return self * o
    
    def __truediv__(self, o):
        if isinstance(o, Number):
            return Vector3D(self.x / o, self.y / o, self.z / o)
        raise TypeError

    def __str__(self):
        return f"x: {self.x}\ty: {self.y}\tz: {self.z}"
    
    def crossproduct(self, vec):
        if isinstance(vec, Vector3D):
            return Vector3D(
                self.y * vec.z - self.z * vec.y,
                self.z * vec.x - self.x * vec.z,
                self.x * vec.y - self.y * vec.x
            )
        raise TypeError

    def mod(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    def normal(self):
        return self / self.mod()
    
    def distance(self, vec):
        if not isinstance(vec, Vector3D):
            raise TypeError
        return (self - vec).mod()
    
    def apply(self, func):
        return Vector3D(func(self.x), func(self.y), func(self.z))
    
    