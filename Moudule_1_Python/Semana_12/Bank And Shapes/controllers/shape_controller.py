from shapes.circle import Circle
from shapes.square import Square
from shapes.rectangle import Rectangle

def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            else:
                print("Please enter a number greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def handle_shape_creation():
    while True:
        shape_election = input("""\nWhich shape do you want to create?
    Circle [1], Square [2], Rectangle [3]: """)

        if shape_election == "1":
            radius = get_positive_float("Please enter the circle's radius measure: ")
            circle = Circle(radius)
            print(f"Area: {circle.calculate_area():.2f}")
            print(f"Perimeter: {circle.calculate_perimeter():.2f}")

        elif shape_election == "2":
            side = get_positive_float("Please enter the square's side measure: ")
            square = Square(side)
            print(f"Area: {square.calculate_area():.2f}")
            print(f"Perimeter: {square.calculate_perimeter():.2f}")

        elif shape_election == "3":
            width = get_positive_float("Please enter the rectangle's width measure: ")
            height = get_positive_float("Please enter the rectangle's height measure: ")
            rectangle = Rectangle(width, height)
            print(f"Area: {rectangle.calculate_area():.2f}")
            print(f"Perimeter: {rectangle.calculate_perimeter():.2f}")

        else:
            print("Please select a correct option (1, 2, or 3).")

        again = input("Do you want to create another shape? (yes/no): ").strip().lower()
        if again != "yes":
            break
