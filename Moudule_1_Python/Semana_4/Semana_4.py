#Ejercicio_1

#string + string 
resultado1 = "Hola " + "Kevin"  # Resultado: 'Hola Kevin'

# string + int - ERROR: no se pueden sumar tipos distintos
# resultado2 = "Hola" + 5       # TypeError

# int + string - ERROR
# resultado3 = 5 + "Hola"       # TypeError

# list + list - se combinan las listas
resultado4 = [1, 2] + [3, 4]    # Resultado: [1, 2, 3, 4]

# string + list - ERROR
# resultado5 = "Hola" + [1, 2]  # TypeError

# float + int - se suman y el resultado es float
resultado6 = 2.5 + 3           # Resultado: 5.5

# bool + bool - True se considera 1, False es 0
resultado7 = True + True       # Resultado: 2
resultado8 = True + False      # Resultado: 1
resultado9 = False + False     # Resultado: 0
print(f'{resultado1}--{resultado4}--{resultado4}--{resultado6}--{resultado7}--{resultado8}--{resultado9}')

#Ejercicio_2: Cree un programa que le pida al usuario su nombre, apellido, y edad, y muestre 
# si es un bebé, niño, preadolescente, adolescente, adulto joven, adulto, o adulto mayor.

def pedir_edad(): 
    while True: 
        try:
            edad = int(input("Cuál es su edad?"))
            return edad
        except ValueError:
            print("Por favor, ingrese solo números.")    

def clasificar_edad (edad):
    if edad <= 2:
        categoria = 'bebé'
    elif edad >=3 and edad <7:
        categoria = 'niño'
    elif edad >=7 and edad <=11:
        categoria = 'preadolescente'
    elif edad >=12 and edad <19:
        categoria = 'adolescente'
    elif edad >=19 and edad <30:
        categoria = 'adulto'
    elif edad >=31 and edad <60:
        categoria = 'adulto'
    elif edad >=60:
        categoria = 'adulto mayor'
    return  (f'{nombre} {apellido} está en la etapa de {categoria}')

nombre = input("Ingrese su nombre: ")
apellido = input("Ingrese su apellido: ")

while not nombre.isalpha() or not apellido.isalpha(): 
    print("Por favor, ingrese solo letras.")
    nombre = input("Ingrese su nombre: ")
    apellido = input("Ingrese su apellido: ")

edad = pedir_edad()

print(clasificar_edad(edad))

#Ejercicio_3: Cree un programa con un numero secreto del 1 al 10. El programa no debe cerrarse hasta que el usuario adivine el numero.
#Debe investigar cómo generar un número aleatorio distinto cada vez que se ejecute.

import random

def pedir_numero():
    while True:
        try:
            numero = int(input("Ingrese un número del 1 al 10: "))
            if 1 <= numero <= 10:
                return numero
            else:
                print("El número debe estar entre 1 y 10.")
        except ValueError:
            print("Por favor, ingrese solo números.")

contador = 1
numero_secreto = random.randint(1, 10)
numero_usuario = pedir_numero()

while numero_usuario != numero_secreto:
    contador += 1
    print("¡Intenta de nuevo, no te rindas!")
    numero_usuario = pedir_numero()

print(f'¡Felicidades! Adivinaste el número secreto: {numero_secreto} en {contador} intento(s)')

#Cree un programa que le pida tres números al usuario y muestre el mayor.

def numeros():
    while True:
        try: 
            num_uno = int(input("Ingrese el primer número: "))
            num_dos = int(input("Ingrese el segundo número: "))
            num_tres = int(input("Ingrese el tercer número: "))
            return num_uno, num_dos, num_tres
        except ValueError:
            print("Por favor, ingrese solo números.")

valores = numeros()
mayor = max(valores)

print(f'El número mayor es: {mayor}')

5. #Dada `n` cantidad de notas de un estudiante, calcular:
    #1. Cuantas notas tiene aprobadas (mayor a 70).
    #2. Cuantas notas tiene desaprobadas (menor a 70).
    #3. El promedio de todas.
    #4. El promedio de las aprobadas.
    #5. El promedio de las desaprobadas.###

contador = int(input("¿Cuántas notas en total vas a ingresar?: "))

aprobadas = []
reprobadas = []

def notas():
    i = 0
    while i < contador:
        try:
            nota = int(input(f"Ingrese la nota #{i+1}: "))
            if 0 <= nota <= 100:
                if nota >= 70:
                    aprobadas.append(nota)
                else:
                    reprobadas.append(nota)
                i += 1
            else:
                print("La nota debe estar entre 0 y 100.")
        except ValueError:
            print("Las notas deben ser números. Intente de nuevo.")

def promedios(aprobadas, reprobadas):
    total_notas = len(aprobadas) + len(reprobadas)

    if total_notas > 0:
        prom_total = (sum(aprobadas) + sum(reprobadas)) / total_notas
    else:
        prom_total = 0

    prom_aprobadas = sum(aprobadas) / len(aprobadas) if aprobadas else 0
    prom_reprobadas = sum(reprobadas) / len(reprobadas) if reprobadas else 0
    print(f"El promedio total es: {prom_total:.2f}")
    print(f"El promedio de las notas aprobadas es: {prom_aprobadas:.2f}")
    print(f"El promedio de las notas reprobadas es: {prom_reprobadas:.2f}")

notas()
print(f'\nNotas aprobadas: {aprobadas}')
print(f'Notas reprobadas: {reprobadas}')

promedios(aprobadas, reprobadas)

