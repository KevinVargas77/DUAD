
from exercises.ex_1_2 import Circle, Bus, Person
from exercises.human_ex_4 import Head, Arm, Leg, Torso, LowerBody, Human

def run_ex_1_2():
    print("\nExercise 1: Circle")
    radius = float(input("Enter the radius of the circle: "))
    circle = Circle(radius)
    print(f"The area is: {circle.get_area():.2f}")

    print("\nExercise 2: Bus Simulation")
    max_passengers = int(input("Maximum passengers for the bus: "))
    bus = Bus(max_passengers)

    while True:
        action = input("Add [a], Remove [r], Show [s], Exit [e]: ").lower()
        if action == "a":
            ticket = input("Enter passenger ticket: ")
            person = Person(ticket)
            bus.add_passenger(person)
        elif action == "r":
            ticket = input("Enter passenger ticket to remove: ")
            person = Person(ticket)
            bus.remove_passenger(person)
        elif action == "s":
            print(f"Passengers: {[p.ticket for p in bus.passengers]}")
        elif action == "e":
            break
        else:
            print("Invalid option.")


def run_ex_4_human():
    print("\nExercise 4: Human Assembly")

    head = Head("brown", "small", "normal", "2", "short", "beard")
    left_arm = Arm("left", "bicep", "forearm", "hand", 5)
    right_arm = Arm("right", "bicep", "forearm", "hand", 5)
    torso = Torso(left_arm, right_arm)
    left_leg = Leg("left", "thigh", "calf", "foot", 5)
    right_leg = Leg("right", "thigh", "calf", "foot", 5)
    lower_body = LowerBody(left_leg, right_leg)
    human = Human(head, torso, lower_body, "white",1.75)

    print("Human Summary:")
    print(f"Skin color: {human.skin_color}")
    print(f"Height: {human.height}")
    print(f"Head hair: {human.head.head_hair}, Facial hair: {human.head.facial_hair}")
    print(f"Eyes: {human.head.eyes}, Nose: {human.head.nose}, Mouth: {human.head.mouth}")

