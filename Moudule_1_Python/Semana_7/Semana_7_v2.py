def get_number():
    try:
        return int(input("Enter #: "))
    except ValueError:
        print("Insert a valid number")
        return get_number()

def calculate(current, operator):
    number = get_number()
    if operator == "+":
        return current + number
    elif operator == "-":
        return current - number
    elif operator == "*":
        return current * number
    elif operator == "/":
        if number == 0:
            print("Cannot divide by zero")
            return current
        return current / number

def main():
    try:
        actual_number = int(input("Please enter a number: "))
        while True:
            operator = input("+, -, *, /, or delete (#) to reset or quit: ")
            if operator in ["+", "-", "*", "/"]:
                actual_number = calculate(actual_number, operator)
            elif operator == "#":
                actual_number = 0
                print("Result reset to 0.")
                actual_number = int(input("Please enter a new starting number: "))
            else:
                print("Invalid operator. Please choose +, -, *, /, or #.")
                continue

            print(f"Current result: {actual_number}")

    except Exception as ex:
        print(f"There was an error: {ex}")

main()
