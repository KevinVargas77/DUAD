"""
Big O Notation – Glossary

Big O notation describes how the execution time or memory usage of an algorithm grows based on the size of the input (n).

O(1) – Constant time
    - Execution time does not change regardless of input size.
    - Example: accessing a specific element by index in a list.

O(log n) – Logarithmic time
    - Very efficient. Each step cuts the problem in half.
    - Example: binary search in a sorted list.

O(n) – Linear time
    - Time grows proportionally with the size of the input.
    - Example: iterating over a list once.

O(n log n) – Linearithmic time
    - Slower than O(n), but faster than O(n²).
    - Example: efficient sorting algorithms like Merge Sort or Quick Sort.

O(n²) – Quadratic time
    - Time grows with the square of the input size.
    - Typically caused by nested loops.
    - Example: comparing all pairs in a list.

O(n³) – Cubic time
    - Very inefficient. Comes from three nested loops.
    - Example: generating all combinations of elements from three lists.

O(2^n) – Exponential time
    - Execution time doubles with each increase in n.
    - Very expensive even for small inputs.
    - Example: brute-force algorithms in complex problems.

O(n!) – Factorial time
    - Extremely inefficient. Time explodes even for small values of n.
    - Example: generating all possible permutations of n elements.

General rule: The lower the complexity, the more efficient the algorithm.
"""
