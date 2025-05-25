from binary_tree import Node as TreeNode
from linked_list import Stack
from deque import Deque

if __name__ == "__main__":
    print("\n--- Binary Tree ---")
    root = TreeNode("A")
    root.left = TreeNode("B")
    root.right = TreeNode("C")
    root.left.left = TreeNode("D")
    root.right.left = TreeNode("E")
    root.right.right = TreeNode("F")
    root.print_tree()

    print("\n--- Stack (Linked List) ---")
    stack = Stack()
    stack.push(10)
    stack.push(20)
    stack.push(30)
    stack.print_stack()

    print("\n--- Deque ---")
    deque = Deque()
    deque.push_left("Left1")
    deque.push_right("Right1")
    deque.push_left("Left2")
    deque.push_right("Right2")

    current = deque.head
    while current:
        print(current.value, end=" <-> ")
        current = current.next
    print("None")
