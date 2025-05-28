class Node:
    def __init__(self,value):
        self.value = value 
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self,value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            return
        
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node 

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result

def bubble_sort_linked_list(linked_list):
    if not linked_list.head or not linked_list.head.next:
        return

    swapped = True
    while swapped:
        swapped = False
        current = linked_list.head

        while current.next:
            if current.value > current.next.value:
                # Swap the values (not the nodes)
                current.value, current.next.value = current.next.value, current.value
                swapped = True
            current = current.next


def run_linked_list_bubble_sort():
    print("\n--- LinkedList: Bubble Sort ---")
    ll = LinkedList()

    for value in [10, 2, 7, 1, 5, 3, 6 , 8 ,9]: 
        ll.append(value)
    print("Before sorting:")
    print(ll.to_list())
      
    bubble_sort_linked_list(ll)
    print("After sorting:")
    print(ll.to_list())
