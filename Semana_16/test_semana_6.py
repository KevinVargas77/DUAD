import pytest
from semana_6 import numbers_sum, reverse_str,count_case,is_palindrome

def test_numbers_sum(): # Exercise 3: (sum)
    #Arrange 
    numbers = [4,5,7,8]
    #Act 
    result = numbers_sum(numbers)
    #Assert 
    assert result == 24


def test_is_palindrome_true():
    #Arrange 
    text = "civic"
    #Act 
    result = is_palindrome(text)
    #Assert 
    assert result is True


def test_reverse_str():
    #Arrange
    text = "Yo hago yoga hoy"
    #Act 
    result = reverse_str(text)
    #Assert 
    assert result == "yoh agoy ogah oY"


def test_count_case():
    #Arrange
    text = "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!"
    #Act 
    result = count_case(text)
    #Assert 
    assert result == (2, 30)
