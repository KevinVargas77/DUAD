# big_o_analysis

# 1. Bubble Sort
def bubble_sort(list_to_sort):
    for i in range(len(list_to_sort)):                   # O(n)
        for j in range(len(list_to_sort) - 1):           # O(n)
            if list_to_sort[j] > list_to_sort[j + 1]:    # O(1)
                list_to_sort[j], list_to_sort[j + 1] = list_to_sort[j + 1], list_to_sort[j]
# Overall Time Complexity: O(n^2)
# Space Complexity: O(1)


# 2. Print each number multiplied by 2
def print_numbers_times_2(numbers_list):
    for number in numbers_list:        # O(n)
        print(number * 2)              # O(1)
# Overall Time Complexity: O(n)
# Space Complexity: O(1)


# 3. Check if any element is common between two lists
def check_if_lists_have_an_equal(list_a, list_b):
    for element_a in list_a:               # O(n)
        for element_b in list_b:           # O(m)
            if element_a == element_b:     # O(1)
                return True
    return False
# Overall Time Complexity: O(n * m)
# Space Complexity: O(1)


# 4. Print up to 10 elements of a list
def print_10_or_less_elements(list_to_print):
    list_len = len(list_to_print)                  # O(1)
    for index in range(min(list_len, 10)):         # O(1) → max 10 iterations
        print(list_to_print[index])                # O(1)
# Overall Time Complexity: O(1)
# Space Complexity: O(1)


# 5. Generate all possible trios from 3 lists
def generate_list_trios(list_a, list_b, list_c):
    result_list = []                                           # O(1)
    for element_a in list_a:                                   # O(n)
        for element_b in list_b:                               # O(m)
            for element_c in list_c:                           # O(p)
                result_list.append(f'{element_a} {element_b} {element_c}')  # O(1)
    return result_list
# Overall Time Complexity: O(n * m * p)
# Space Complexity: O(n * m * p)
