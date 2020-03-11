#End up using my own custom Queue with abilty to insert elements to the front of the queue. 
# Technicaly it's a Deque, but I'm using only insert to the front ability

class Node:
    def __init__(self,item):
        self.item = item
        self.next = None

class Queue:
    #Constructor
    #Space and time complexity is O(1)
    def __init__(self):
        self.head = None
        self.tail = None
        self.num_elements = 0

    #Inserts the element to the queue
    #Space and time complexity is O(1)
    def enqueue(self, item):
        if self.tail is None:
            self.tail = Node(item)
            self.head = self.tail
            self.num_elements += 1
            return
        
        self.tail.next = Node(item)
        self.tail = self.tail.next
        self.num_elements += 1
      
    #inserts the element to the front of the queue. Using to reset truck queue
    #Space and time complexity is O(1)
    def front(self, item):
        if self.head is None:
            self.head = Node(item)
            self.tail = self.head
            self.num_elements += 1
            return
        node = Node(item)
        node.next = self.head
        self.head = node
        self.num_elements += 1

    #Space and time complexity is O(1)
    def size(self):
        return self.num_elements

    #Returns the element in the head of the queue
    #Space and time complexity is O(1)
    def dequeue(self):
        if self.head is None:
            return None
        value = self.head.item
        self.head = self.head.next
        self.num_elements -= 1
        return value