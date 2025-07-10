class Node: 
    def __init__(self,value):
        self.value = value
        self.next = None

class Stack:
    def __init__(self):
        self.top = None

    def push(self,value):
        new_node = Node(value)
        new_node.next = self.top
        self.top = new_node
    
    def pop(self):
        if self.top is None:
            print("The stack is empty")
            return None
        node_to_remove = self.top #Pros use temp =
        self.top = self.top.next 
        return node_to_remove.value # temp.value
    
    def print_stack(self):
        current = self.top
        while current: 
            print(current.value)
            current = current.next 
