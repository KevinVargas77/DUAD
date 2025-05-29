def bubble_sort(list_to_sort):
    n_reps = len(list_to_sort) - 1
    for outer_i in range(n_reps):
        has_made_changes = False
        for i in range(n_reps - outer_i):
            current_element = list_to_sort[i]
            next_element = list_to_sort[i + 1]

            print(f"--Iteration {outer_i}, comparing: {current_element} and {next_element}")
            if current_element > next_element:
                print("Swapping current with next element")
                list_to_sort[i], list_to_sort[i + 1] = next_element, current_element
                has_made_changes = True
        if not has_made_changes:
            break
    return list_to_sort


def bubble_sort_reverse(list_to_sort):
    n_reps = len(list_to_sort) - 1
    for outer_i in range(n_reps):
        has_made_changes = False
        for i in range(n_reps, outer_i, -1):
            current_element = list_to_sort[i]
            prev_element = list_to_sort[i - 1]

            print(f"--Iteration {outer_i}, comparing: {current_element} and {prev_element}")
            if current_element > prev_element:
                print("Swapping current with previous element")
                list_to_sort[i], list_to_sort[i - 1] = prev_element, current_element
                has_made_changes = True
        if not has_made_changes:
            break
    return list_to_sort


def bubble_even_reverse(list_to_sort):
    n_reps = len(list_to_sort) - 1
    for outer_i in range(n_reps):
        has_made_changes = False
        for i in range(n_reps, outer_i, -1):
            current_element = list_to_sort[i]
            prev_element = list_to_sort[i - 1]

            print(f"--Iteration {outer_i}, comparing: {current_element} and {prev_element}")
            if current_element % 2 == 0 and prev_element % 2 != 0:
                print("Swapping even with odd number")
                list_to_sort[i - 1], list_to_sort[i] = current_element, prev_element
                has_made_changes = True
        if not has_made_changes:
            break
    return list_to_sort

