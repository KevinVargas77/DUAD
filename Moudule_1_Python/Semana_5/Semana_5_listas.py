1#. Cree un programa que itere e imprima los valores de dos listas del mismo tamaño al mismo tiempo.
  #  1. Ejemplos:

first_list = ['Hay', 'en', 'que', 'iteracion', 'indices', 'muy']
second_list = ['casos', 'los', 'la', 'por', 'es', 'util']

for index, word in enumerate(first_list): 
    print(first_list[index],second_list[index])
print()

third_list = ['I', 'someday', 'have', 'beautiful']
fourth_list = ['know', "you'll", 'a', 'life']

#Da el mismo resultado, segun a lo que leo es mejor usar lo anterior.  
for i in range(len(third_list)):
    print(third_list[i],fourth_list[i])
print()    

#Cree un programa que itere e imprima un string letra por letra de derecha a izquierda.

my_string = 'Pizza con piña'
my_copy = my_string[::-1] #[ start primer letra: stop ultima letra : step reversa]
for letter in my_copy:
    print(letter)
print()

#Cree un programa que intercambie el primer y ultimo elemento de una lista. Debe funcionar con 
# listas de cualquier tamaño.

# Esta fue la solucion que logre crear pero no me siento comodo con esta solucion, 
# no se si es la mejor.
my_list = [4, 3, 6, 1, 7]
invert_list = my_list[:]
invert_list[0],invert_list[-1] = invert_list[-1],invert_list[0]
print(my_list)
print(invert_list)
print()

#Cree un programa que elimine todos los números impares de una lista.

my_list_2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
all_numbers = my_list_2[:] # Paso innecesario, solo queria practicar lo de copiar una lista que lo vi en un video hoy. 
odd_numbers = []

for i, number in enumerate(all_numbers): 
    if all_numbers[i] % 2 != 0:
        odd_numbers.append(number)
print(odd_numbers)

#Cree un programa que le pida al usuario 10 números, y al final le muestre todos los números que 
# ingresó, seguido del numero ingresado más alto.

numbers = []

print('Please enter your 10 numbers:')

for i in range(10):
    num = int(input(f'Number {i+1}: '))
    numbers.append(num)
max_number = max(numbers)
print(f'Your numbers are {numbers}, and the highest of them is: {max_number}')
