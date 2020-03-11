class EmptyBucket:
    pass

class CustomHashTable:
    def __init__(self, init_capacity=8):
        #creating two options for the array
        self.EMPTY_SINCE_START = EmptyBucket()
        self.EMPTY_AFTER_REMOVAL = EmptyBucket()
        self.num_elements = 0
        self.key_list = []
        
        #initializing array with empty bucket objects
        self.table = [self.EMPTY_SINCE_START] * init_capacity
    
    def insert(self, key, item):
        #checks to see if table is full, resize it with double capacity
        if self.num_elements == len(self.table) - int(len(self.table) / 4):
            self.resize()
        
        count = 0
        #iterating through the range of the table to find right bucket to place the item in.
        while True:
            #on each iteration calculating the bucket number
            #checks if the bucket is empty
            hash_code = self.calculate_hash(count, key)
            if type(self.table[hash_code]) is EmptyBucket:
                self.table[hash_code] = (key, item)
                self.key_list.append(key)
                self.num_elements += 1
                return True
            count += 1
        
    
    def search(self, key):
        #iterating through the range of the table to find right bucket to place the item in.
        for i in range(len(self.table)):
            #on each iteration calculating the bucket number
            hash_code = self.calculate_hash(i, key)

            if  type(self.table[hash_code]) is not EmptyBucket:
                if self.table[hash_code][0] == key:
                    return self.table[hash_code][1]
        return None
    
    def remove(self, key):
        #iterating through the range of the table to find right bucket to place the item in.
        for i in range(len(self.table)):
            #on each iteration calculating the bucket number
            hash_code = self.calculate_hash(i, key)
            
            if  type(self.table[hash_code]) is not EmptyBucket:
                if self.table[hash_code][0] == key:
                    self.table[hash_code] = self.EMPTY_AFTER_REMOVAL
                    self.key_list.remove(key)
                    self.num_elements -= 1

    #helper methods
    def calculate_hash(self, index, key):
        return (hash(key) + self.hash_2(key) * index) % len(self.table)

    def keys(self):
        return self.key_list

    def resize(self):
        new_table = [self.EMPTY_SINCE_START] * (len(self.table) * 2)
        for i in range(len(self.table)):
            new_table[i] = self.table[i]
        self.table = new_table

    def hash_2(self, key):
        return 7 - hash(key) % 7

    #override to string method
    def __str__(self):
        str_list = ""
        for key in self.key_list:
            str_list += str(self[key]) + "\n" 
        return str_list
    #gives ability to use brakets [] to access the element in the hash table
    def __getitem__(self, key):
       return self.search(key)

    #gives ability to use brakets [] to set the element in the hash table
    def __setitem__(self, key, item):
        return self.insert(key, item)

    def __contains__(self, key):
        return key in self.key_list