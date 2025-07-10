
def first_name(name): # Exercise 1: (functions)
    full_text = f"Hello, my name is {name}\n{last_name()}"
    return full_text


def last_name():
    return "Vargas"


def even_numbers(numbers): #Exercise 2: (scope)
    even_num = [] 

    for num in numbers:
        if num % 2 == 0:
            even_num.append(num) 
    return even_num


def odd_numbers(numbers):
    odd_num = []

    for num in numbers:
        if num % 2 != 0:
            odd_num.append(num)
    return odd_num


def numbers_sum(numbers): # Exercise 3: (sum)
    total = 0

    for num in numbers:
        total += num
    return total


def reverse_str(text): #Exercise 4: (Reverse String) 
    print(text[::-1])


def count_case(text):  #Exercise 5: (total lower and upper case)
    total_upper = 0
    total_lower = 0

    for letter in text:
        if letter.isupper(): #new methods learned .isupper and .islower
            total_upper += 1
        elif letter.islower():
            total_lower += 1

    print(f"Uppercase letters: {total_upper}")
    print(f"Lowercase letters: {total_lower}")


def sort_lyrics (lyrics): #Exercise 6 sort a string
    word_list = lyrics.split('-') #new methods learned .split, ''.join
    word_list.sort()
    return '-'.join(word_list)


def prime_numbers(numbers):  # Exercise 7 ### comments added to understand the logical 
    primes = []  # List to store prime numbers
    for num in numbers:
        if num > 1:  # Prime numbers must be greater than 1
            # Try dividing the number by every integer from 2 up to but not including itself (num+1)
            for i in range(2, num):
                if num % i == 0:
                    # If divisible by any of these, it's not a prime number
                    break  # Exit the loop early does not make sense to continue
            else:
                # If the loop didn't break, the number is prime and be added to the list
                primes.append(num)
    return primes


def main():
    name = "Kevin"
    exercise_one = first_name(name)
    numbers = list(range(1, 26))
    lyrics_snippet = "wanna-wish-it-all-away-don’t-wanna-stay"

    print("\n=== Exercise 1 ===")
    print(exercise_one)

    print("\n=== Exercise 2 ===")
    print("Even numbers:", even_numbers(numbers))
    print("Odd numbers:", odd_numbers(numbers))

    print("\n=== Exercise 3 ===")
    print("Sum of numbers:", numbers_sum(numbers))

    print("\n=== Exercise 4 ===")
    print("Reversed string exercise 1:")
    reverse_str(exercise_one)

    print("\n=== Exercise 5 ===")
    count_case(exercise_one)

    print("\n=== Exercise 6 ===")
    print("Sorted lyrics snippet:", sort_lyrics(lyrics_snippet))

    print("\n=== Exercise 7 ===")
    print("Prime numbers in list:", prime_numbers(numbers))


main()
