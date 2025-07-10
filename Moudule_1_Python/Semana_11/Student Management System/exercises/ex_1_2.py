""""Exercises 1,2 - week 11"""

import math

class Circle:
    def __init__(self,radius): 
        self.radius = radius

    def get_area(self):
        area = math.pi * self.radius ** 2
        return area

class Person:
    def __init__(self, ticket):
        self.ticket = ticket

class Bus:
    def __init__(self,max_passengers):
        self.max_passengers = max_passengers
        self.passengers = []
    

    def add_passenger(self,person):
        if len(self.passengers) >= self.max_passengers:
            print("The bus is full, cannot board.")
        else: 
            self.passengers.append(person)
            print(f"Passenger with ticket {person.ticket} boarded.")
    
    
    def remove_passenger(self, person):
        for p in self.passengers:
            if p.ticket == person.ticket:
                self.passengers.remove(p)
                print(f"Passenger with ticket {p.ticket} has left the bus.")
                return
        print("This passenger is not on the bus.")

