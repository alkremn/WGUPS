from heapq import heappush, heappop, heapify

class Node:
    def __init__(self,item):
        self.item = item
        self.next = None

class Queue:
    
    def __init__(self):
        self.head = None
        self.tail = None
        self.num_elements = 0

    def enqueue(self, item):
        if self.tail is None:
            self.tail = Node(item)
            self.head = self.tail
            self.num_elements += 1
            return
        
        self.tail.next = Node(item)
        self.tail = self.tail.next
        self.num_elements += 1
      
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

    def size(self):
        return self.num_elements

    def dequeue(self):
        if self.head is None:
            return None
        value = self.head.item
        self.head = self.head.next
        self.num_elements -= 1
        return value
    
    def is_empty(self):
        return self.num_elements == 0

    def __str__(self):
        current = self.head
        values = ""
        while current:
            values += str(current.item) + "\n"
            current = current.next
        return values