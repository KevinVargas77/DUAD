import math
from shapes.shape import Shape

class Rectangle(Shape):
    def __init__(self,width,height):
        self.width = width
        self.height = height 
    

    def calculate_area(self):
        return self.width * self.height 
    
    
    def calculate_perimeter(self):
        return 2 * (self.width + self.height)
    