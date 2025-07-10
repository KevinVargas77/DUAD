# main.py

from bubble_sort import bubble_sort, bubble_sort_reverse, bubble_even_reverse
from linkedlist_bubble import LinkedList, bubble_sort_linked_list, run_linked_list_bubble_sort

def run_array_bubble_sort():
    print("\n--- Array: Bubble Sort ---")
    numbers = [8, 3, 1, 6, 4]
    print("Before:", numbers)
    bubble_sort(numbers)
    print("After: ", numbers)

def run_array_bubble_reverse():
    print("\n--- Array: Bubble Sort (Descending) ---")
    numbers = [1, 2, 3, 4, 5]
    print("Before:", numbers)
    bubble_sort_reverse(numbers)
    print("After: ", numbers)

def run_array_bubble_even():
    print("\n--- Array: Bubble Even to Front ---")
    numbers = [1, 2, 3, 4, 5, 6, 7]
    print("Before:", numbers)
    bubble_even_reverse(numbers)
    print("After: ", numbers)

if __name__ == "__main__":
    run_array_bubble_sort()
    run_array_bubble_reverse()
    run_array_bubble_even()
    run_linked_list_bubble_sort()

