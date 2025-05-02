def Addition (actual_number):
    try:
        number = int(input(f'Enter #:'))
        actual_number += number
        return actual_number
    except ValueError: 
        print(f'Insert a valid number')


def subtraction (actual_number):
    try:
        number = int(input(f'Enter #:'))
        actual_number -= number
        return actual_number
    except ValueError: 
        print(f'Insert a valid number')


def division (actual_number):
    try:
        number = int(input(f'Enter #:'))
        actual_number = actual_number / number 
        return actual_number
    except ValueError: 
        print(f'Insert a valid number')


def multiplication (actual_number):
    try:
        number = int(input(f'Enter #:'))
        actual_number = actual_number * number 
        return actual_number
    except ValueError: 
        print(f'Insert a valid number')


def main():
    try:
        actual_number = int(input('Please enter a number:'))
        while True:
            operator = input("+, -, *, /, or delete (#) to reset or quit: ")
            
            if operator == "+":
                actual_number = Addition(actual_number)
            elif operator == "-":
                actual_number = subtraction(actual_number)
            elif operator == "*":
                actual_number = multiplication(actual_number)
            elif operator == "/":
                actual_number = division(actual_number)
            elif operator == "#":
                actual_number = 0
                print("Result reset to 0.")
                actual_number = int(input("Please enter a new starting number: "))
            else:
                print("Invalid operator. Please choose +, -, *, /, or #.")
                continue
            
            print(f'Current result: {actual_number}')
    
    except Exception as ex:
        print(f'There was an error: {ex}')


main()