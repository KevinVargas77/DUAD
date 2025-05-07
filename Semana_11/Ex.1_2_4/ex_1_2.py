import math

class Circle:
    def __init__(self,radius): 
        self.radius = radius

    def get_area(self):
        area = math.pi * self.radius ** 2
        return area


class Bus:
    def __init__(self,max_passengers):
        self.max_passengers = max_passengers
    
    def AddPassenger(self):
        if counter < self.max_passengers:
            counter += 1
        elif counter >= self.max_passengers:
        print("The bus is full, cannot aboard")
