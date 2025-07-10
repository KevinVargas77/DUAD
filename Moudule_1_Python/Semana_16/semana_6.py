
def numbers_sum(numbers): 
    total = 0

    for num in numbers:
        total += num
    return total


def reverse_str(text):
    return text[::-1]


def count_case(text):
    total_upper = 0
    total_lower = 0

    for letter in text:
        if letter.isupper():
            total_upper += 1
        elif letter.islower():
            total_lower += 1
    return total_upper, total_lower


def is_palindrome(text):
    if text == text[::-1]:
        return True
    return False 


def reverse_str(text):
    return(text[::-1])


def count_case(text):  
    total_upper = 0
    total_lower = 0

    for letter in text:
        if letter.isupper(): 
            total_upper += 1
        elif letter.islower():
            total_lower += 1
    return total_upper, total_lower


def sort_lyrics(lyrics): 
    word_list = lyrics.split('-') 
    word_list.sort()
    return '-'.join(word_list)


def prime_numbers(numbers):  
    primes = []  
    for num in numbers:
        if num > 1:  
            for i in range(2, num):
                if num % i == 0:
                    break  
            else:
                primes.append(num)
    return primes
