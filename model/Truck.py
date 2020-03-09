from datastractures.Queue import Queue
from model.Status import Status

class Truck:
    def __init__(self, id, start_time, load):
        self.id = id
        self.start_time = start_time
        self.SPEED = 18
        self.load_size = 0
        self.distance = 0
        self.dist_to_hub = 0
        self.loadQueue = self.load_truck(load)
        self.delivered = []
        self.total_distance = 0
    

    def load_truck(self, load):
        loadQueue = Queue()
        for package in load[0]:
            loadQueue.enqueue(package)
            self.load_size += 1
        
        self.dist_to_hub = load[1]
        return loadQueue

    def calculate_distance(self, current_time):
        time_span = current_time - self.start_time
        total_mins = time_span.get_mins()
        return (total_mins / 60) * self.SPEED
    

    def calculate_delivery(self, distance):
        list_ids = []
        while self.loadQueue.head:
            loc_dist = self.loadQueue.head.item[1]
            distance -= loc_dist
            if distance < 0:
                distance += loc_dist
                break
            package = self.loadQueue.dequeue()
            self.total_distance += package[1]
            list_ids.append((package, distance))
            self.delivered.append(package)
       
        self.total_distance += distance
        if self.loadQueue.head is None:
            self.total_distance += self.dist_to_hub
        
        return list_ids
    
    def deliver_all(self):
        while self.loadQueue.head:
            package = self.loadQueue.dequeue()
            self.total_distance += package[1]
            self.delivered.append(package)
        self.total_distance += self.dist_to_hub
        return self.total_distance
            
    