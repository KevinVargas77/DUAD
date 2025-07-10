#Ejercicio_1

#string + string 
result1 = "Hello " + "Kevin"  # Result: 'Hello Kevin'

# string + int - ERROR: can't add different types
# result2 = "Hello" + 5       # TypeError

# int + string - ERROR
# result3 = 5 + "Hello"       # TypeError

# list + list - lists are combined
result4 = [1, 2] + [3, 4]    # Result: [1, 2, 3, 4]

# string + list - ERROR
# result5 = "Hello" + [1, 2]  # TypeError

# float + int - results in float
result6 = 2.5 + 3           # Result: 5.5

# bool + bool - True is 1, False is 0
result7 = True + True       # Result: 2
result8 = True + False      # Result: 1
result9 = False + False     # Result: 0
print(f'{result1}--{result4}--{result4}--{result6}--{result7}--{result8}--{result9}')

#Ejercicio_2: Cree un programa que le pida al usuario su nombre, apellido, y edad, y muestre 
# si es un bebé, niño, preadolescente, adolescente, adulto joven, adulto, o adulto mayor.

def ask_age(): 
    while True: 
        try:
            age = int(input("What is your age?"))
            return age
        except ValueError:
            print("Please enter numbers only.")    

def classify_age(age):
    if age <= 2:
        category = 'baby'
    elif age >=3 and age <7:
        category = 'child'
    elif age >=7 and age <=11:
        category = 'preteen'
    elif age >=12 and age <19:
        category = 'teenager'
    elif age >=19 and age <30:
        category = 'young adult'
    elif age >=31 and age <60:
        category = 'adult'
    elif age >=60:
        category = 'senior adult'
    return  (f'{first_name} {last_name} is in the {category} stage')

first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")

while not first_name.isalpha() or not last_name.isalpha(): 
    print("Please enter letters only.")
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")

age = ask_age()

print(classify_age(age))

#Ejercicio_3: Cree un programa con un numero secreto del 1 al 10. El programa no debe cerrarse hasta que el usuario adivine el numero.
#Debe investigar cómo generar un número aleatorio distinto cada vez que se ejecute.

import random

def ask_number():
    while True:
        try:
            number = int(input("Enter a number from 1 to 10: "))
            if 1 <= number <= 10:
                return number
            else:
                print("The number must be between 1 and 10.")
        except ValueError:
            print("Please enter numbers only.")

attempts = 1
secret_number = random.randint(1, 10)
user_number = ask_number()

while user_number != secret_number:
    attempts += 1
    print("Try again, don't give up!")
    user_number = ask_number()

print(f'Congratulations! You guessed the secret number: {secret_number} in {attempts} attempt(s)')

#Ejercicio_4: Cree un programa que le pida tres números al usuario y muestre el mayor.

def get_numbers():
    while True:
        try: 
            num_one = int(input("Enter the first number: "))
            num_two = int(input("Enter the second number: "))
            num_three = int(input("Enter the third number: "))
            return num_one, num_two, num_three
        except ValueError:
            print("Please enter numbers only.")

values = get_numbers()
largest = max(values)

print(f'The largest number is: {largest}')

#Ejercicio_5: Dada `n` cantidad de notas de un estudiante, calcular:
#1. Cuantas notas tiene aprobadas (mayor a 70).
#2. Cuantas notas tiene desaprobadas (menor a 70).
#3. El promedio de todas.
#4. El promedio de las aprobadas.
#5. El promedio de las desaprobadas.

total = int(input("How many grades will you enter in total?: "))

passing = []
failing = []

def enter_grades():
    i = 0
    while i < total:
        try:
            grade = int(input(f"Enter grade #{i+1}: "))
            if 0 <= grade <= 100:
                if grade >= 70:
                    passing.append(grade)
                else:
                    failing.append(grade)
                i += 1
            else:
                print("The grade must be between 0 and 100.")
        except ValueError:
            print("Grades must be numbers. Try again.")

def averages(passing, failing):
    total_grades = len(passing) + len(failing)

    if total_grades > 0:
        total_avg = (sum(passing) + sum(failing)) / total_grades
    else:
        total_avg = 0

    passing_avg = sum(passing) / len(passing) if passing else 0
    failing_avg = sum(failing) / len(failing) if failing else 0
    print(f"The overall average is: {total_avg:.2f}")
    print(f"The average of passing grades is: {passing_avg:.2f}")
    print(f"The average of failing grades is: {failing_avg:.2f}")

enter_grades()
print(f'\nPassing grades: {passing}')
print(f'Failing grades: {failing}')

averages(passing, failing)
