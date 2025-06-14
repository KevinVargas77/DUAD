from bubble_sort import bubble_sort

def test_bubble_sort_sort_list():
    # Arrange
    data = [5, 2, 1, 4]
    # Act
    result = bubble_sort(data)
    # Assert
    assert result == [1, 2, 4, 5]


def test_bubble_sort_long_list():
    # Arrange
    data = [42, 1, 17, 63, 5, 91, 33, 26, 9, 80, 15, 2, 11, 100, 56, 78, 67, 49, 7, 31,
               73, 86, 28, 39, 19, 60, 92, 14, 4, 53, 21, 13, 30, 38, 66, 77, 10, 6, 8, 12,
               16, 18, 20, 22, 23, 24, 25, 27, 29, 32, 34, 35, 36, 37, 40, 41, 43, 44, 45, 46,
               47, 48, 50, 51, 52, 54, 55, 57, 58, 59, 61, 62, 64, 65, 68, 69, 70, 71, 72, 74,
               75, 76, 79, 81, 82, 83, 84, 85, 87, 88, 89, 90, 93, 94, 95, 96, 97, 98, 99, 3]
    # Act
    result = bubble_sort(data)
    # Assert
    assert result == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
            21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
            41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
            61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80,
            81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]


def test_bubble_sort_blank_list():
    #Arrange
    data = []
    #Act
    result = bubble_sort(data)
    #Assert
    assert result == []


def test_bubble_sort_not_list():
    #Arrange 
    data = (5, 2, 1, 4)
    #Act 
    result = bubble_sort(data)
    #Assert 
    assert result == (1, 2, 4, 5)