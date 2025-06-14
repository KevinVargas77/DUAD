import pytest
from semana_6 import numbers_sum, reverse_str,count_case,is_palindrome,sort_lyrics,prime_numbers

#---test exercise # 1 ---
def test_numbers_sum_positives(): 
    #Arrange 
    numbers = [4,5,7,8]
    #Act 
    result = numbers_sum(numbers)
    #Assert 
    assert result == 24


def test_numbers_sum_negatives(): 
    #Arrange 
    numbers = [-10,-20,-30,-40]
    #Act 
    result = numbers_sum(numbers)
    #Assert 
    assert result == -100


def test_numbers_sum_zeros(): 
    #Arrange 
    numbers = [0,0,0,0,0,0]
    #Act 
    result = numbers_sum(numbers)
    #Assert 
    assert result == 0

### --- Extra ---
def test_is_palindrome_true():
    #Arrange 
    text = "civic"
    #Act 
    result = is_palindrome(text)
    #Assert 
    assert result is True


#--- test exercise #2 ---
def test_reverse_str_yoga():
    #Arrange
    text = "Yo hago yoga hoy"
    #Act 
    result = reverse_str(text)
    #Assert 
    assert result == "yoh agoy ogah oY"


def test_reverse_str_hola():
    #Arrange
    text = "hola"
    #Act 
    result = reverse_str(text)
    #Assert 
    assert result == "aloh"


def test_reverse_str_python():
    #Arrange
    text = "Python"
    #Act 
    result = reverse_str(text)
    #Assert 
    assert result == "nohtyP"


#--- test exercise #3 ---
def test_count_case_abeja():
    #Arrange
    text = "¿Dónde guardas el sushi, Samurái?"
    #Act 
    result = count_case(text)
    #Assert 
    assert result == (2, 24)


def test_count_case_samurai():
    #Arrange
    text = "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!"
    #Act 
    result = count_case(text)
    #Assert 
    assert result == (2, 30)


def test_count_case_robot():
    #Arrange
    text = "¡Corre, que viene el robot del futuro!"
    #Act 
    result = count_case(text)
    #Assert 
    assert result == (1, 28)


#--- test exercise #4 ---   
def test_sort_lyrics_alive():
    #Arrange
    lyrics = "son-I-I-am-still-alive"
    #Act
    result = sort_lyrics(lyrics)
    #Assert 
    assert result == "I-I-alive-am-son-still"


def test_sort_lyrics_black():
    #Arrange 
    lyrics = "tattooed-everything-all-I-know"
    #Act
    result = sort_lyrics(lyrics)
    #Assert 
    assert result == "I-all-everything-know-tattooed"


def test_sort_lyrics_black():
    #Arrange 
    lyrics = "tattooed-everything-all-I-know"
    #Act
    result = sort_lyrics(lyrics)
    #Assert 
    assert result == "I-all-everything-know-tattooed"


#--- test exercise #4 ---
def test_prime_numbers_mixed(): 
    #Arrage
    numbers = [1, 4, 6, 7, 13, 9, 67]
    #Act
    result = prime_numbers(numbers)
    #Assert 
    assert result == [7, 13, 67]


def test_prime_numbers_no_primes(): 
    #Arrage
    numbers = [1, 4, 6, 8, 9, 10]
    result = prime_numbers(numbers)
    #Assert 
    assert result == []


def test_prime_numbers_just_primes(): 
    #Arrage
    numbers = [2, 3, 5, 7]
    result = prime_numbers(numbers)
    #Assert 
    assert result == [2, 3, 5, 7]
