class Node:
    def __init__(self,value):
        self.value = value
        self.next = None
        self.prev = None 
    
class Deque:
    def __init__(self):
        self.head = None 
        self.tail = None

    def push_left(self,value):
        new_node = Node(value)

        if self.head is None:  # si está vacío
            self.head = new_node
            self.tail = new_node
        else: 
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node 

    def push_right(self,value):
        new_node = Node(value)

        if self.head is None:  # si está vacío
            self.head = new_node
            self.tail = new_node
        else: 
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node 

    def pop_left(self):

        if self.head is None:  # si está vacío
            print("the Deque is empty")
            return None
        node_to_remove = self.head
        self.head = self.head.next
        
        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None

        return node_to_remove.value
    
    def pop_right(self):

        if self.tail is None:  # si está vacío
            print("the Deque is empty")
            return None
        node_to_remove = self.tail
        self.tail = self.tail.prev
        
        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None

        return node_to_remove.value

def print(self):
    if self.head is None:
        print("The Deque is empty")
        return

    current = self.head
    while current is not None:
        print(current.value, end=" -> ")
        current = current.next
    print("None")

def print_reverse(self):
    if self.tail is None:
        print("The Deque is empty")
        return

    current = self.tail
    while current is not None:
        print(current.value, end=" <- ")
        current = current.prev
    print("None")
