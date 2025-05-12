import math 
from shapes.shape import Shape

class Square(Shape):
    def __init__(self,side):
        self.side = side 


    def calculate_area(self):
        return self.side ** 2
    

    def calculate_perimeter(self):
        return 4 * self.side 
    